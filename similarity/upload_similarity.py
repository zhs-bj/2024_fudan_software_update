from py2neo import Node, Relationship, Graph, Subgraph, NodeMatcher
import pandas as pd
from tqdm import tqdm
import re
import numpy as np

# with neo4j running
graph = Graph("bolt://parthub:7687", auth=("neo4j", "igem2024")) # TO BE MODIFIED
node_matcher = NodeMatcher(graph)

def gradient_color_generate(time: str):
    from datetime import datetime
    import matplotlib as mpl
    begin_time = datetime.strptime('2004-1-1', r'%Y-%m-%d')
    try:
        exact_time = datetime.strptime(time, r'%Y-%m-%d')
    except:
        exact_time = datetime.strptime('2004-1-1', r'%Y-%m-%d')
    now = datetime.now()
    max_interavl = now - begin_time
    interval = now - exact_time
    norm = mpl.colors.Normalize(vmin=0, vmax=max_interavl.days)
    cmap = mpl.colormaps.get_cmap('plasma')
    hex_rgb = mpl.colors.rgb2hex(cmap(norm(interval.days)))
    return hex_rgb

# Delete previous graph
# query = '''
# CALL gds.graph.drop('parthub')
# '''
# graph.run(query)

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
        if part_node is None or len(text_embedding) <= 2:
            continue
        success_hits += 1
        part_node['textEmbedding'] = text_embedding
print('Total parts:', total_parts)
print('Success hits:', success_hits)
print(f'Mapping seq embeddings to nodes success ratio: {success_hits / total_parts * 100}%')


print('Creating graph...')
# create graph
query = """
CALL gds.graph.project(
'parthub',
'Part',
'refers to',
{
    relationshipProperties: 'weight'
}
)
"""
graph.run(query)

print('Calculating PageRanks...')
# calculate PageRanks
query = '''
CALL gds.pageRank.write('parthub', {
maxIterations: 20,
dampingFactor: 0.85,
writeProperty: 'pagerank',
relationshipWeightProperty: 'weight'
})
YIELD nodePropertiesWritten, ranIterations
'''
graph.run(query)

# get max pagerank and min pagerank
query = '''
MATCH (n:Part)
RETURN max(n.pagerank) AS max_val, min(n.pagerank) AS min_val
'''
graph.run(query)

# generate nodesize
query = '''
MATCH (n:Part)
SET n.nodesize = (n.pagerank - 0.15000000000000002) / (46.258541601845714 - 0.15000000000000002) * 90 + 30
'''
graph.run(query)

print('Running Louvain...')
# run Louvain method
query = '''
CALL gds.louvain.write('parthub', {
writeProperty: 'community',
relationshipWeightProperty: 'weight'
})
'''
graph.run(query)

print('Done!')