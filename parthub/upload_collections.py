from py2neo import Node, Relationship, Graph, Subgraph
import pandas as pd
from tqdm import tqdm
import re
import numpy as np
from datetime import datetime
import matplotlib as mpl

# with neo4j running
graph = Graph("bolt://parthub:7687", auth=("neo4j", "igem2024")) # TO BE MODIFIED
graph.delete_all()

query= '''
CALL gds.graph.exists('parthub')
  YIELD exists
RETURN exists
'''
parthub_exists = graph.run(query).data()[0]['exists']
if parthub_exists:
    print('Graph parthub already exists, deleting it...')
    query = '''
    CALL gds.graph.drop('parthub')
    '''
    graph.run(query)

def get_node_color(time: str, is_basic: bool):
    begin_time = datetime.strptime('2004-1-1', r'%Y-%m-%d')
    try:
        exact_time = datetime.strptime(time, r'%Y-%m-%d')
    except:
        exact_time = datetime.strptime('2004-1-1', r'%Y-%m-%d')
    now = datetime.now()
    max_interavl = now - begin_time
    interval = now - exact_time
    norm = mpl.colors.Normalize(vmin=0, vmax=max_interavl.days)
    if is_basic:
        cmap = mpl.colors.LinearSegmentedColormap.from_list('basic_color', ['#6e6dda', '#cacaf6'])
    else:
        cmap = mpl.colors.LinearSegmentedColormap.from_list('composite_color', ['#0987db', '#b4dbf4'])
    hex_rgb = mpl.colors.rgb2hex(cmap(norm(interval.days)))
    return hex_rgb

# Delete previous graph
# query = '''
# CALL gds.graph.drop('parthub')
# '''
# graph.run(query)

fout = open('./similarity/data/seqdump.fasta', 'w')
part_node_dict = {}
for yr in range(2004, 2024): # TO BE MODIFIED (2024)
    print(f'Uploading {yr}...', flush=True)
    data = pd.read_csv(f'./parthub/collections/{yr}collection.csv')
    part_list = []
    relationship_list = []
    for i in data.index:
        part_num = str(data['part_num'].values[i])
        part_name = str(data['part_name'].values[i])
        part_url = str(data['part_url'].values[i])
        part_desc = str(data['short_desc'].values[i])
        part_type = str(data['part_type'].values[i])
        part_team = str(data['team'].values[i])
        part_sequence = str(data['sequence'].values[i])
        part_contents = str(re.sub(' Sequence and Features', '', str(data['contents'].values[i])))
        part_released = str(data['released'].values[i])
        part_sample = str(data['sample'].values[i])
        part_twins = str(data['twins'].values[i])
        part_assemble = str(data['assemble_std'].values[i])
        part_used = str(data['parts_used'].values[i])
        part_using = str(data['using_parts'].values[i])
        part_using_deep = str(data['using_parts_deep'].values[i])
        part_len = str(data['len'].values[i])
        part_date = str(data['date'].values[i])
        part_isfavorite = str(data['isfavorite'].values[i])
        part_year = str(data['year'].values[i])
        part_designer = str(data['designer'].values[i])
        part_category = str(data['category'].values[i])
        try:
            part_used_list = part_used.split(' ')
            part_using_list = part_using.split(' ')
            part_using_deep_list = part_using_deep.split(' ')
            part_twins_list = part_twins.split(' ')
            if part_used == 'None' or part_used == '' or part_used == 'N o n e' or part_used.lower() == 'nan':
                part_used_list = []
            if part_using == 'self' or part_using == '' or part_using.lower() == 'nan':
                part_using_list = []
            if part_twins == 'None' or part_twins == '' or part_twins == 'N o n e' or part_twins.lower() == 'nan':
                part_twins_list = []
            if part_using_deep == 'self' or part_using_deep == '' or part_using_deep.lower() == 'nan':
                part_using_deep_list = []
        except:
            part_used_list = []
            part_using_list = []
            part_twins_list = []
            part_using_deep_list = []
        part_is_basic = (len(part_using_deep_list) == 0)
        part_node = Node('Part', number=str(part_num), name=part_name, url=part_url, description=part_desc, type=part_type,
                        team=part_team, sequence=part_sequence, contents=part_contents, released=part_released,
                        sample=part_sample, assemble=part_assemble, length=part_len, date=part_date,
                        isfavorite=str(part_isfavorite), twins=part_twins_list, twins_num=str(len(part_twins_list)),
                        cited_by=part_used_list, year=part_year, cites=str(len(part_used_list)), ref=part_using_list, deep_subparts=part_using_deep_list,
                        citing=str(len(part_using_list)), designer=part_designer, prweight=max(1,len(part_used_list) * 0.5+len(part_using_list)+0.75 * len(part_twins_list)),
                        color=get_node_color(part_date, part_is_basic), category=part_category)
        part_list.append(part_node)
        part_node_dict.update({str(part_num): part_node})
        fout.write(f'>{part_num}\n{part_sequence}\n')
    twins_set = set()
    for pNode in part_list:
        if pNode['ref']:
            for ref_part in pNode['ref']:
                try:
                    pNode1 = part_node_dict[ref_part]
                    relationShip = Relationship(pNode, 'refers to', pNode1)
                    relationShip["weight"] = pNode['prweight']
                    relationship_list.append(relationShip)
                except:
                    pass
        if pNode['twins']:
            for twin_part in pNode['twins']:
                try:
                    pNode2 = part_node_dict[twin_part]
                    if pNode2['number'] != pNode['number']:
                        if set([pNode2['number'],pNode['number']]) not in twins_set:
                            relationShip = Relationship(pNode, 'twins', pNode2)
                            relationship_list.append(relationShip)
                            twins_set.add(set([pNode2['number'],pNode['number']]))
                except:
                    pass
        if pNode['cited_by']:
            for cite_part in pNode['cited_by']:
                try:
                    pNode3 = part_node_dict[cite_part]
                    relationShip = Relationship(pNode3, 'refers to', pNode)
                    relationShip["weight"] = pNode3['prweight']
                    relationship_list.append(relationShip)
                except:
                    pass
    relationship_list = list(set(relationship_list))
    
    subgraph = Subgraph(part_list, relationship_list)
    tx = graph.begin()
    tx.create(subgraph)
    graph.commit(tx)

fout.close()

print('Creating graph...', flush=True)
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

print('Calculating PageRanks...', flush=True)
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

# generate nodesize
query = '''
MATCH (n:Part)
SET n.nodesize = (n.pagerank - 0.15000000000000002) / (46.258541601845714 - 0.15000000000000002) * 90 + 30
'''
graph.run(query, flush=True)

print('Running Louvain...')
# run Louvain method
query = '''
CALL gds.louvain.write('parthub', {
writeProperty: 'community',
relationshipWeightProperty: 'weight'
})
'''
graph.run(query)

# print('Calculating KNN...', flush=True)
# Calculate KNN
# query = '''
# CALL gds.knn.write('parthub', {
#     writeRelationshipType: 'SIMILAR',
#     writeProperty: 'score',
#     similarityCutoff: 0.75,
#     topK: 5,
#     randomSeed: 233,
#     concurrency: 1,
#     nodeProperties: ['textEmbedding']
# })
# YIELD nodesCompared, relationshipsWritten
# '''
# graph.run(query)

print('Done!')