import numpy as np
import pandas as pd
from flask import jsonify
from py2neo import Node, Graph, NodeMatcher
from burden_calculator import BurdenCalculator

graph = Graph("bolt://parthub:7687", auth=("neo4j", "igem2024"), name="neo4j")
node_matcher = NodeMatcher(graph)

def read_basic_part_csv():
    part_types = ['promoter', 'RBS', 'CDS']
    res_dict = {}
    for part_type in part_types:
        try:
            df = pd.read_csv(f'./burden/data/{part_type.lower()}s.tsv', sep='\t', index_col=0, header=None)
        except:
            return jsonify({'message': f'Failed to read {part_type.lower()}s.tsv'}), 400
        res_dict[part_type] = [{'name': df.index[i], 'seq': df.iloc[i, 0]} for i in range(len(df))]
    return jsonify(res_dict), 200

def parse_basic_part(curPart: Node):
    registry_type = curPart['type']
    part_type = ''
    if registry_type == 'Promoter' or registry_type == 'Regulatory':
        part_type = 'promoter'
    elif registry_type == 'RBS':
        part_type = 'RBS'
    elif registry_type == 'Coding':
        part_type = 'CDS'
    elif registry_type == 'Translational_Unit':
        start_codon = curPart['sequence'].find('atg')
        if start_codon == -1:
            return [None]
        curPart_rbs = curPart.copy()
        curPart_rbs['name'] += '(RBS)'
        curPart_rbs['type'] = 'RBS'
        curPart_cds = curPart.copy()
        curPart_cds['name'] += '(CDS)'
        curPart_cds['type'] = 'Coding'
        curPart_rbs['sequence'] = curPart['sequence'][:start_codon]
        curPart_cds['sequence'] = curPart['sequence'][start_codon:]
        return parse_basic_part(curPart_rbs) + parse_basic_part(curPart_cds)
    if part_type != '':
        name = curPart['number'] + ": " + curPart['name']
        if len(name) > 50:
            name = name[:47] + '...'
        return [{'type': part_type, 'info': {
            'name': name,
            'seq': curPart['sequence']
        }}]
    else:
        return [None]

def get_basic_parts(part_num: str):
    curPart = node_matcher.match("Part", number=part_num).first()
    assert type(curPart['deep_subparts']) == list
    if curPart is None:
        return jsonify({'message': f'Part {part_num} not found'}), 404
    basic_parts = []
    if len(curPart['deep_subparts']) > 0:
        for subpart_num in curPart['deep_subparts']:
            subpart = node_matcher.match("Part", number=subpart_num).first()
            if subpart is None:
                continue
            basic_parts.extend(parse_basic_part(subpart))
    else:
        basic_parts.extend(parse_basic_part(curPart))
    basic_parts = [part for part in basic_parts if part is not None]
    return jsonify({'parts': basic_parts}), 200

def calc_burden(parts: list[dict]):
    pass