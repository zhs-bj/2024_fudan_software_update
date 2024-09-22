import numpy as np
import pandas as pd
import os
import re
from py2neo import Node, Graph, NodeMatcher

graph = Graph("bolt://parthub:7687", auth=("neo4j", "igem2024"), name="neo4j")
node_matcher = NodeMatcher(graph)

BASE = 1.5

def calc_cat_score(category: str):
    score = 0
    for cat in category.split(' '):
        if not cat:
            continue
        labels = cat.split('/')[2:]
        score += (BASE ** len(labels) - 1) / (BASE - 1)
    return score

def calc_common_cat_score(category1: str, category2: str):
    com_score = 0
    for cat in category2.split(' '):
        labels = cat.split('/')[2:]
        label = '/'
        weight = 1
        for i, l in enumerate(labels):
            label += '/' + l
            if label in category1:
                com_score += weight
                weight *= BASE
            else:
                break
    mx_score = np.maximum(calc_cat_score(category1), calc_cat_score(category2))
    if mx_score == 0:
        return 0
    return com_score / mx_score

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
    parts = parts - set([i['m.number'] for i in parts_using + parts_used + parts_twins] + [curPart])

    # Calculate the similarity score
    results = []
    for part in parts:
        matchedNode = node_matcher.match("Part", number=part).first()
        if matchedNode is None:
            continue
        res_dict = {"part": part, "seq_score": 0.0, 'cat_score': 0.0}
        max_len = np.maximum(len(curSeq), len(matchedNode["sequence"]))
        for i in df[df.iloc[:, 1] == part].index:
            res_dict["seq_score"] = np.maximum(res_dict["seq_score"], float(df.iloc[i, 2]) / 100 * 0.7 + float(df.iloc[i, 3]) / max_len * 0.3)
        matchedCat = matchedNode["category"]
        res_dict["cat_score"] = calc_common_cat_score(curCat, matchedCat)
        res_dict["overall_score"] = 0.8 * res_dict["seq_score"] + 0.2 * res_dict["cat_score"]
        results.append(res_dict)
    results.sort(key=lambda x: x["overall_score"], reverse=True)
    results = results[:30]
    for part_info in results:
        part = part_info["part"]
        (part1, part2) = (curPart, part) if curPart < part else (part, curPart)
        query = """
        MATCH (n: Part {number: '"""+ part1 + """'}), (m: Part {number: '"""+ part2 + """'})
        MERGE (n)-[r:similar {seq_score:"""+ str(part_info["seq_score"]) + \
        """,cat_score:"""+ str(part_info["cat_score"]) + \
        """,overall_score:""" + str(part_info["overall_score"]) + """}]->(m)
        """
        graph.run(query)
    return results