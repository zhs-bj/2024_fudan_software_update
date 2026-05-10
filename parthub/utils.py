"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : utils.py
@Author : Hongchen Chen / Assistant
@Time : 2024/9/10 22:50
"""
import os
import re
from typing import Any
from time import time

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from flask import jsonify, Response
from py2neo import Node, Graph, NodeMatcher
import pandas as pd

import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from config import parthub_config

graph = Graph(parthub_config["serverUrl"], auth=("neo4j", "igem2024"), name="neo4j")
node_matcher = NodeMatcher(graph)


# ---------------------------------------------------------------------------
# Lucene query helpers
# ---------------------------------------------------------------------------

def escape_lucene(text: str) -> str:
    """
    Escape special characters in Lucene query syntax.
    If the text contains spaces, wrap it in double quotes.
    """
    if not text:
        return ""
    if ' ' in text:
        escaped = text.replace('"', '\\"')
        return f'"{escaped}"'
    special_chars = r'+-&|!(){}[]^"~*?:\\/'
    return re.sub(r'([{}])'.format(re.escape(special_chars)), r'\\\1', text)


def build_fulltext_query(search_key: str, search_type: str) -> str:
    """
    Build a Lucene full-text query string.
    Single word -> field:word~
    Multiple words -> field:word1~ AND field:word2~ ...
    """
    words = search_key.split()
    if len(words) == 1:
        return f"{search_type}:{escape_lucene(words[0])}~"
    terms = [f"{search_type}:{escape_lucene(w)}~" for w in words]
    return " AND ".join(terms)


# ---------------------------------------------------------------------------
# Node result processing
# ---------------------------------------------------------------------------

KEYS_REQUIRED = [
    'year', 'team', 'designer', 'type', 'number', 'name', 'contents',
    'cites', 'twins_num', 'length', 'isfavorite', 'released', 'date',
    'url', 'pagerank', 'community'
]


def _process_node_records(records, search_type: str) -> list[dict[str, Any]]:
    """Common logic to convert Neo4j records to dict list."""
    node_dic_list = []
    for record in records:
        node = record if isinstance(record, Node) else record.get('node')
        score = 0.0 if isinstance(record, Node) else record.get('score', 0.0)
        if node is None:
            continue
        node_dic = dict(node)
        node_dic = {key: value for key, value in node_dic.items() if key in KEYS_REQUIRED}
        node_dic['_score'] = float(score)
        if search_type == 'contents':
            node_dic['matchedContents'] = content_match(node_dic.get('contents', ''))
            node_dic.pop('contents', None)
        else:
            node_dic['matchedContents'] = node_dic.get('contents', '')[:200]
            node_dic.pop('contents', None)
        node_dic_list.append(node_dic)
    return node_dic_list


def content_match(content: str) -> str:
    """
    :param content: content of selected node
    :return: content preview
    """
    if not content or content == 'nan':
        return ''
    content_lst = content.split(' ')
    if len(content_lst) <= 40:
        return ' '.join(content_lst)
    return ' '.join(content_lst[:40]) + '...'


# ---------------------------------------------------------------------------
# Full-text search (Phase 1)
# ---------------------------------------------------------------------------

def search_node(search_key: str, search_type: str) -> list[dict[str | Any, str | Any]] | None:
    if search_type == 'sequence':
        return search_sequence(search_key)

    # Try full-text index first
    result = search_node_fulltext(search_key, search_type)
    if result is not None:
        return result

    # Fallback to legacy regex matching
    return search_node_legacy(search_key, search_type)


def search_node_fulltext(search_key: str, search_type: str) -> list[dict[str | Any, str | Any]] | None:
    query_str = build_fulltext_query(search_key, search_type)
    cypher = """
    CALL db.index.fulltext.queryNodes('partSearch', $query)
    YIELD node, score
    RETURN node, score
    LIMIT 1000
    """
    try:
        results = graph.run(cypher, query=query_str).data()
    except Exception as e:
        # Index may not exist or other error; silently fallback
        print(f"[Fulltext search warning] {e}")
        return None

    # Index exists but no matches -> return empty list (do not fallback to legacy)
    if not results:
        return []
    return _process_node_records(results, search_type)


def search_node_legacy(search_key: str, search_type: str) -> list[dict[str | Any, str | Any]] | None:
    """Original regex-based search (fallback)."""
    query = f"_.{search_type} =~ '(?i).*{re.escape(search_key)}.*'"
    nodes = list(node_matcher.match("Part").where(query))
    if not nodes:
        return None
    return _process_node_records(nodes, search_type)


# ---------------------------------------------------------------------------
# Sequence search with BLAST fallback
# ---------------------------------------------------------------------------

def search_sequence(search_key: str) -> list[dict[str | Any, str | Any]] | None:
    """
    1. Exact match (including reverse complement).
    2. If no results, fallback to BLAST short-sequence alignment.
    """
    search_key = search_key.lower()
    key_inverse = search_key.replace("a", "t").replace("t", "a").replace("c", "g").replace("g", "c")

    sequence_query = "_.sequence =~ '(?i).*key.*' OR _.sequence =~ '(?i).*inverse.*'"
    sequence_query_temp = re.sub('key', search_key, sequence_query)
    sequence_query = re.sub('inverse', key_inverse, sequence_query_temp)
    nodes = list(node_matcher.match("Part").where(sequence_query))

    if nodes:
        return _process_node_records(nodes, 'sequence')

    # Fallback to BLAST for fuzzy sequence matching
    return blast_short_match(search_key)


def blast_short_match(seq: str) -> list[dict[str | Any, str | Any]] | None:
    """Run blastn-short to tolerate mismatches in short sequences."""
    seq = seq.upper()
    cur_time = int(time() * 1e6)
    temp_query = f"./similarity/data/temp_query_{cur_time}.fasta"
    query_ans = f"./similarity/data/query_ans_{cur_time}.txt"

    try:
        with open(temp_query, "w") as fout:
            fout.write(f">query\n{seq}\n")

        cmd = (
            f"./blast+/bin/blastn -query {temp_query} "
            f"-db ./similarity/data/seqdump.fasta "
            f"-out {query_ans} -evalue 1e-3 -outfmt 6 "
            f"-max_target_seqs 50"
        )
        if len(seq) <= 32:
            cmd += " -task blastn-short"

        status = os.system(cmd)
        if status != 0:
            return None

        try:
            df = pd.read_csv(query_ans, sep="\t", header=None)
        except pd.errors.EmptyDataError:
            return []

        parts = set(df.iloc[:, 1])
        results = []
        for part in parts:
            matched_node = node_matcher.match("Part", number=part).first()
            if matched_node is None:
                continue
            node_dic = dict(matched_node)
            node_dic = {key: value for key, value in node_dic.items() if key in KEYS_REQUIRED}
            node_dic['matchedContents'] = node_dic.get('contents', '')[:200]
            node_dic.pop('contents', None)
            node_dic['_score'] = 0.0
            results.append(node_dic)
        return results
    finally:
        if os.path.exists(temp_query):
            os.remove(temp_query)
        if os.path.exists(query_ans):
            os.remove(query_ans)


# ---------------------------------------------------------------------------
# Multiple keyword search
# ---------------------------------------------------------------------------

def multiple_search(kwd_list: list[str], search_type: str, flag: str) -> None | list[dict] | list[Any] | Any:
    if len(kwd_list) < 2:
        return None

    # Try full-text index first
    result = multiple_search_fulltext(kwd_list, search_type, flag)
    if result is not None:
        return result

    # Fallback to legacy manual intersection/union
    return multiple_search_legacy(kwd_list, search_type, flag)


def multiple_search_fulltext(kwd_list: list[str], search_type: str, flag: str) -> None | list[dict] | list[Any] | Any:
    grouped_terms = []
    for kwd in kwd_list:
        words = kwd.split()
        if len(words) == 1:
            grouped_terms.append(f"{search_type}:{escape_lucene(words[0])}~")
        else:
            sub_terms = [f"{search_type}:{escape_lucene(w)}~" for w in words]
            grouped_terms.append(f"({' AND '.join(sub_terms)})")

    lucene_flag = "AND" if flag == 'AND' else "OR"
    query_str = f" {lucene_flag} ".join(grouped_terms)

    cypher = """
    CALL db.index.fulltext.queryNodes('partSearch', $query)
    YIELD node, score
    RETURN node, score
    LIMIT 1000
    """
    try:
        results = graph.run(cypher, query=query_str).data()
    except Exception as e:
        print(f"[Fulltext multi-search warning] {e}")
        return None

    # Index exists but no matches -> return empty list (do not fallback)
    if not results:
        return []
    return _process_node_records(results, search_type)


def multiple_search_legacy(kwd_list: list[str], search_type: str, flag: str) -> None | list[dict] | list[Any] | Any:
    """Original manual AND/OR logic (fallback)."""
    res = []
    if flag == 'AND':
        res = search_node_legacy(kwd_list[0], search_type)
        num_list = get_num_list(res)
        for kwd in kwd_list[1:]:
            if res:
                res = [i for i in search_node_legacy(kwd, search_type) if i.get('number') in num_list]
                num_list = get_num_list(res)
            else:
                return None
    else:
        num_list = []
        for kwd in kwd_list:
            res = res + [i for i in search_node_legacy(kwd, search_type) if i.get('number') not in num_list]
            num_list = get_num_list(res)
    return res


def get_num_list(node_dic_list: list[dict]) -> list[str]:
    return [i.get('number') for i in node_dic_list]


# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------

def sort_node(node_dic_lst: list[dict]):
    """
    Sort by combined score (Lucene relevance * PageRank weighting),
    then deduplicate by community.
    """
    for item in node_dic_lst:
        lucene_score = item.pop('_score', 0.0)
        pagerank = float(item.get('pagerank', 0.15))
        # Normalize pagerank roughly to [0, 1]
        normalized_pr = max(0.0, min(1.0, (pagerank - 0.15) / 50.0))
        item['_combined_score'] = lucene_score * (1 + normalized_pr * 2)

    sorted_node_dic_lst = sorted(node_dic_lst, key=lambda x: x['_combined_score'], reverse=True)

    for item in sorted_node_dic_lst:
        item.pop('_combined_score', None)

    seen_communities = set()
    unique_community_list = []
    else_list = []
    for item in sorted_node_dic_lst:
        if item["community"] not in seen_communities:
            unique_community_list.append(item)
            seen_communities.add(item["community"])
        else:
            else_list.append(item)
    return unique_community_list + else_list


# ---------------------------------------------------------------------------
# Public API entry
# ---------------------------------------------------------------------------

def parthub_search(search_key: str, search_type: str) -> tuple[Response, int]:
    if ' AND ' in search_key:
        kwd_list = search_key.split(' AND ')
        all_res = multiple_search(kwd_list, search_type, 'AND')
    elif ' OR ' in search_key:
        kwd_list = search_key.split(' OR ')
        all_res = multiple_search(kwd_list, search_type, 'OR')
    else:
        all_res = search_node(search_key, search_type)
    if all_res:
        return jsonify(sort_node(all_res)), 200
    else:
        return jsonify({'message': f'No search result found: key={search_key}, type={search_type}'}), 200


# ---------------------------------------------------------------------------
# File generation helpers
# ---------------------------------------------------------------------------

def init_create() -> None:
    if not os.path.exists(r'./parthub'):
        os.makedirs(r'./parthub')


def create_parthub_seq_file(part_id: str) -> str:
    init_create()
    filename = part_id + '.gb'
    query = """
    MATCH (p:Part {number: 'part_id'})
    RETURN p.sequence;
    """
    query = re.sub('part_id', part_id, query)
    sequence = str(graph.run(query).evaluate())
    seq_record = SeqRecord(Seq(sequence), id=part_id)
    seq_record.annotations["molecule_type"] = "DNA"
    with open(os.path.join(r'./parthub', filename), 'w') as f:
        SeqIO.write(seq_record, f, "genbank")
    return os.path.join(r'./parthub', filename)


def get_part_id(name: str) -> str:
    query = """
    MATCH (p:Part {number: 'part_id'})
    RETURN ID(p);
    """
    query = re.sub('part_id', name, query)
    part_id = str(graph.run(query).evaluate())
    return part_id
