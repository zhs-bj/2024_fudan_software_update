"""
Semantic search for iGEM parts using sentence-transformers embeddings.
"""
import os
import json
import re
import numpy as np
from typing import Any

from py2neo import Graph, NodeMatcher

import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from config import parthub_config

DATA_DIR = os.path.join(os.path.dirname(__file__), 'semantic_data')
EMBEDDINGS_FILE = os.path.join(DATA_DIR, 'embeddings.npy')
INDEX_FILE = os.path.join(DATA_DIR, 'part_index.json')
TEXTS_FILE = os.path.join(DATA_DIR, 'part_texts.json')

# Lazy-loaded model and embeddings
_model = None
_embeddings = None
_part_index = None
_part_texts = None

_graph = None
_node_matcher = None


def _get_graph():
    global _graph, _node_matcher
    if _graph is None:
        _graph = Graph(parthub_config["serverUrl"], auth=("neo4j", "igem2024"), name="neo4j")
        _node_matcher = NodeMatcher(_graph)
    return _graph, _node_matcher


KEYS_REQUIRED = [
    'year', 'team', 'designer', 'type', 'number', 'name', 'contents',
    'cites', 'twins_num', 'length', 'isfavorite', 'released', 'date',
    'url', 'pagerank', 'community'
]


def _ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return _model


def _load_embeddings():
    global _embeddings, _part_index, _part_texts
    if _embeddings is None:
        if not os.path.exists(EMBEDDINGS_FILE):
            return False
        _embeddings = np.load(EMBEDDINGS_FILE)
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            _part_index = json.load(f)
        if os.path.exists(TEXTS_FILE):
            with open(TEXTS_FILE, 'r', encoding='utf-8') as f:
                _part_texts = json.load(f)
        else:
            _part_texts = [None] * len(_part_index)
    return True


def _fetch_all_parts_text() -> tuple[list[str], list[str]]:
    """
    Fetch all Part nodes from Neo4j and build searchable text.
    Returns (texts, part_numbers).
    """
    cypher = """
    MATCH (p:Part)
    RETURN p.number AS number, p.name AS name, p.contents AS contents
    """
    graph, _ = _get_graph()
    results = graph.run(cypher).data()

    texts = []
    numbers = []
    for record in results:
        number = record.get('number') or ''
        name = record.get('name') or ''
        contents = record.get('contents') or ''
        if contents == 'nan':
            contents = ''
        # Combine name and contents for embedding
        combined = f"{name}. {contents}".strip()
        if not combined or not number:
            continue
        texts.append(combined)
        numbers.append(number)

    return texts, numbers


def build_semantic_index():
    """
    Offline script: generate embeddings for all parts and save to disk.
    Run this once (or whenever parts data changes).
    """
    _ensure_data_dir()
    print("[Semantic Search] Fetching parts from Neo4j...")
    texts, numbers = _fetch_all_parts_text()
    print(f"[Semantic Search] Total parts to index: {len(texts)}")

    if not texts:
        raise RuntimeError("No parts found in Neo4j. Check your database connection.")

    model = _get_model()
    print("[Semantic Search] Encoding parts (this may take a few minutes)...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    np.save(EMBEDDINGS_FILE, embeddings)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(numbers, f)
    with open(TEXTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(texts, f)

    print(f"[Semantic Search] Index saved to {DATA_DIR}")
    print(f"[Semantic Search] Embeddings shape: {embeddings.shape}")


def _cosine_similarity(query_vec: np.ndarray, embeddings: np.ndarray) -> np.ndarray:
    """
    Compute cosine similarity between query vector and all embeddings.
    """
    # Normalize embeddings
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings_norm = embeddings / np.clip(norms, a_min=1e-10, a_max=None)

    query_norm = query_vec / np.clip(np.linalg.norm(query_vec), a_min=1e-10, a_max=None)

    return embeddings_norm @ query_norm


def semantic_search(query: str, top_k: int = 50) -> list[dict[str, Any]]:
    """
    Search parts by natural language description.
    Returns list of part dicts sorted by semantic similarity.
    """
    if not _load_embeddings():
        raise RuntimeError(
            "Semantic index not found. Please run 'python -m parthub.build_semantic_index' first."
        )

    model = _get_model()
    query_vec = model.encode(query, convert_to_numpy=True)

    similarities = _cosine_similarity(query_vec, _embeddings)
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        part_number = _part_index[idx]
        _, node_matcher = _get_graph()
        matched_node = node_matcher.match("Part", number=part_number).first()
        if matched_node is None:
            continue
        node_dic = dict(matched_node)
        node_dic = {key: value for key, value in node_dic.items() if key in KEYS_REQUIRED}
        node_dic['matchedContents'] = node_dic.get('contents', '')[:200]
        node_dic.pop('contents', None)
        node_dic['_score'] = float(similarities[idx])
        results.append(node_dic)

    return results
