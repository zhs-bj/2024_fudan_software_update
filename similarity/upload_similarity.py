from py2neo import Node, Relationship, Graph, Subgraph, NodeMatcher
import pandas as pd
from tqdm import tqdm
import re
import numpy as np

# with neo4j running
graph = Graph("bolt://parthub:7687", auth=("neo4j", "igem2024")) # TO BE MODIFIED
node_matcher = NodeMatcher(graph)

part_nodes = list(node_matcher.match("Part"))
relationship_list = []
total_parts = 0
success_hits = 0
with open('~/fudan2024/similarity/data/seq_embeddings.txt', 'r') as f:
    for i in tqdm(range(70000)): # TO BE MODIFIED
        line = f.readline()[:-1]
        if not line:
            break
        total_parts += 1
        part_num, seq_embedding = line.split(':')
        seq_embedding = list(map(float, seq_embedding.split(' ')))
        part_node = node_matcher.match("Part", number=part_num).first()
        if part_node is None:
            continue
        success_hits += 1
        part_node['seqEmbedding'] = seq_embedding
print('Total parts:', total_parts)
print('Success hits:', success_hits)
print(f'Mapping seq embeddings to nodes success ratio: {success_hits / total_parts * 100}%')

total_parts = 0
success_hits = 0
with open('~/fudan2024/similarity/data/text_embeddings.csv', 'r') as f:
    for i in tqdm(range(70000)): # TO BE MODIFIED
        line = f.readline()[:-1]
        if not line:
            break
        total_parts += 1
        part_num, text_embedding = line.split(',')
        text_embedding = list(map(float, text_embedding.split(' ')))
        part_node = node_matcher.match("Part", number=part_num).first()
        if part_node is None:
            continue
        success_hits += 1
        part_node['textEmbedding'] = text_embedding
print('Total parts:', total_parts)
print('Success hits:', success_hits)
print(f'Mapping seq embeddings to nodes success ratio: {success_hits / total_parts * 100}%')
