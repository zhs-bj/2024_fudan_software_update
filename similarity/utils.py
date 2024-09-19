import numpy as np
import pandas as pd
import os
import re
from py2neo import Node, Graph, NodeMatcher

graph = Graph("bolt://parthub:7687", auth=("neo4j", "igem2024"), name="neo4j") # TO BE MODIFIED
node_matcher = NodeMatcher(graph)

def query_similarity(curPart: str):
    curNode = node_matcher.match("Part", number=curPart).first()
    if curNode is None:
        return None
    curSeq = curNode["sequence"]
    curCat = curNode["category"]
    with open("./similarity/data/temp_query.fasta", "w") as fout:
        fout.write(f">{curPart}\n{curSeq}\n")
    
    # Run BLAST
    cmd = "./blast+/bin/blastn -query ./similarity/data/temp_query.fasta " \
              "-db ./similarity/data/seqdump.fasta " \
              "-out ./similarity/data/query_ans.txt -evalue 1e-3 -outfmt 6"
    if len(curSeq) <= 32:
        cmd += " -task blastn-short"
    status = os.system(cmd)
    if status != 0:
        return None
    try:
        df = pd.read_csv("./similarity/data/query_ans.txt", sep="\t", header=None)
    except pd.errors.EmptyDataError:
        return []
    
    # Remove parts that refer to or are referred by the current part
    parts = set(df.iloc[:, 1])
    query = "MATCH (n:Part {number: '" + curPart + "'})-[:`refers to`]->{0,100}(m:Part) RETURN m.number"
    parts_using = graph.run(query).data()
    query = "MATCH (n:Part {number: '" + curPart + "'})<-[:`refers to`]-{0,100}(m:Part) RETURN m.number"
    parts_used = graph.run(query).data()
    query = "MATCH (n:Part {number: '" + curPart + "'})-[:twins]-(m:Part) RETURN m.number"
    parts_twins = graph.run(query).data()
    parts = parts - set([i['m.number'] for i in parts_using + parts_used + parts_twins])

    # Calculate the similarity score
    results = []
    for part in parts:
        matchedNode = node_matcher.match("Part", number=part).first()
        if matchedNode is None:
            continue
        matchedCat = matchedNode["category"].split(' ')
        res_dict = {"part": part, "seq_score": 0.0, 'cat_score': 0.0}
        max_len = np.maximum(len(curSeq), len(matchedNode["sequence"]))
        for i in df[df.iloc[:, 1] == part].index:
            res_dict["seq_score"] = np.maximum(res_dict["seq_score"], float(df.iloc[i, 2]) / 100 * 0.7 + float(df.iloc[i, 3]) / max_len * 0.3)
        for cat in matchedCat:
            labels = cat.split('/')[2:]
            label = '/'
            weight = 0.5
            for i, l in enumerate(labels):
                label += '/' + l
                if i == 1:
                    weight = 2
                if label in curCat:
                    res_dict["cat_score"] += weight
                else:
                    break
        results.append(res_dict)
    for part_info in results:
        part = part_info["part"]
        query = """
        MATCH (n: Part {number: '"""+ curPart + """'}), (m: Part {number: '"""+ part + """'})
        MERGE (n)-[r:similar {seq_score:"""+ str(part_info["seq_score"]) + \
        """,cat_score:"""+ str(part_info["cat_score"]) + \
        """,overrall_score:""" + str(part_info["seq_score"] * 0.8 + part_info["cat_score"] * 0.2) + """}]->(m)
        """
        graph.run(query)
    return results