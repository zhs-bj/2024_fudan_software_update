from py2neo import Node, Relationship, Graph, Subgraph
import pandas as pd
from tqdm import tqdm
import re
import numpy as np

# with neo4j running
graph = Graph("bolt://localhost:7687", auth=("neo4j", "igem2024"))
graph.delete_all()

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

for yr in range(2004, 2024):
    print(f'Addressing {yr}...')
    data = pd.read_csv(f'~/fudan/PartHub2/collections/{yr}collection.csv')
    part_node_dict = {}
    part_list = []
    relationship_list = []
    for i in tqdm(data.index):
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
        part_len = str(data['len'].values[i])
        part_date = str(data['date'].values[i])
        part_isfavorite = str(data['isfavorite'].values[i])
        part_year = str(data['year'].values[i])
        part_designer = str(data['designer'].values[i])
        try:
            part_used_list = part_used.split(' ')
            part_using_list = part_using.split(' ')
            part_twins_list = part_twins.split(' ')
            if part_used == 'None' or part_used == '' or part_used == 'N o n e':
                part_used_list = []
            if part_using == 'self' or part_using == '':
                part_using_list = []
            if part_twins == 'None' or part_twins == '' or part_twins == 'N o n e':
                part_twins_list = []
        except:
            part_used_list = []
            part_using_list = []
            part_twins_list = []
        part_node = Node('Part', number=str(part_num), name=part_name, url=part_url, description=part_desc, type=part_type,
                        team=part_team, sequence=part_sequence, contents=part_contents, released=part_released,
                        sample=part_sample, assemble=part_assemble, length=part_len, date=part_date,
                        isfavorite=str(part_isfavorite), twins=part_twins_list, twins_num=str(len(part_twins_list)),
                        cited_by=part_used_list, year=part_year, cites=str(len(part_used_list)), ref=part_using_list,
                        citing=str(len(part_using_list)), designer=part_designer, prweight=max(1,len(part_used_list) * 0.5+len(part_using_list)+0.75 * len(part_twins_list)),
                        color=gradient_color_generate(part_date))
        part_list.append(part_node)
        part_node_dict.update({str(part_num): part_node})
    twins_set_list = []
    twins_node_list = []
    for pNode in tqdm(part_node_dict.values()):
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
                        if set([pNode2['number'],pNode['number']]) not in twins_set_list:
                            relationShip = Relationship(pNode, 'twins', pNode2)
                            relationship_list.append(relationShip)
                            twins_set_list.append(set([pNode2['number'],pNode['number']]))
                except:
                    pass
        if pNode['cited_by']:
            for cite_part in pNode['cited_by']:
                try:
                    pNode3 = part_node_dict[cite_part]
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

# run Louvain method
query = '''
CALL gds.louvain.write('parthub', {
writeProperty: 'community',
relationshipWeightProperty: 'weight'
})
'''
graph.run(query)