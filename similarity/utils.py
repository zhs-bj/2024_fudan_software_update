import numpy as np
import pandas as pd
import os
import re
from py2neo import Node, Graph, NodeMatcher
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from flask import jsonify
from datetime import datetime
from time import time
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from config import parthub_config

graph = Graph(parthub_config["serverUrl"], auth=("neo4j", "igem2024"), name="neo4j")
node_matcher = NodeMatcher(graph)

BASE = 1.5

def calc_common_cat_score(category1: str, category2: str):
    com_score = 0
    for cat in category2.split(' '):
        labels = cat.split('/')[2:]
        label = '/'
        weight = 1
        for l in labels:
            label += '/' + l
            if label in category1:
                com_score += weight
                weight *= BASE
            else:
                break
    return com_score

def query_similarity(curPart: str):
    curNode = node_matcher.match("Part", number=curPart).first()
    if curNode is None:
        return None
    curSeq = curNode["sequence"]
    curCat = curNode["category"]
    curTime = int(time() * 1e6)
    temp_query = f"./similarity/data/temp_query_{curTime}.fasta"
    query_ans = f"./similarity/data/query_ans_{curTime}.txt"
    with open(temp_query, "w") as fout:
        fout.write(f">{curPart}\n{curSeq}\n")
    
    # Run BLAST
    cmd = "./blast+/bin/blastn -query "+temp_query+" " \
              "-db ./similarity/data/seqdump.fasta " \
              "-out "+query_ans+" -evalue 1e-5 -outfmt 6"
    if len(curSeq) <= 32:
        cmd += " -task blastn-short"
    status = os.system(cmd)
    if status != 0:
        return None
    try:
        df = pd.read_csv(query_ans, sep="\t", header=None)
    except pd.errors.EmptyDataError:
        os.remove(temp_query)
        os.remove(query_ans)
        return []
    
    os.remove(temp_query)
    os.remove(query_ans)
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
    try:
        max_bs = float(df.iloc[0, 11])
    except:
        return None
    results = []
    for part in parts:
        matchedNode = node_matcher.match("Part", number=part).first()
        if matchedNode is None:
            continue
        res_dict = {"part": part, "name": matchedNode["name"], "seq_score": 0.0, 'cat_score': 0.0}
        for i in df[df.iloc[:, 1] == part].index:
            identity = float(df.iloc[i, 2])
            bit_score = float(df.iloc[i, 11])
            res_dict["seq_score"] = np.maximum(res_dict["seq_score"],
                                    bit_score / max_bs * 70 + identity / 100 * 30)
        matchedCat = matchedNode["category"]
        res_dict["cat_score"] = calc_common_cat_score(curCat, matchedCat)
        res_dict["overall_score"] = np.minimum(res_dict["seq_score"] + res_dict["cat_score"], 100)
        results.append(res_dict)
    results.sort(key=lambda x: x["overall_score"], reverse=True)
    results = results[:100]
    results_add_to_graph = results[:30]
    for part_info in results_add_to_graph:
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

def parse_part_file(filename: str, part_type: str):
    file_format = filename.rsplit('.', 1)[1].lower()
    try:
        records = list(SeqIO.parse(filename, file_format))
        record = records[0]
        seq = str(record.seq).upper()
    except:
        return jsonify({"message": "File parse error. Please check the file format."}), 400
    return jsonify({"seq": seq}), 200

def add_new_part(part_type: str, seq: str):
    seq = seq.upper()
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    TIME_BASE = 1727325400
    curtime = int((time() - TIME_BASE) * 1000)
    try:
        query = "CREATE (n:Part{number:'New_part_" + str(curtime) + "',name:'" + now + \
            "',type:'" + part_type + "',sequence:'" + seq + "',contents:'',length:" + str(len(seq)) + \
            ",date:'',team:'User',designer:'User',category:'',url:''})"
        graph.run(query)
    except:
        return jsonify({"message": "Failed to add new part"}), 500
    return jsonify({"part_id": "New_part_" + str(curtime)}), 200