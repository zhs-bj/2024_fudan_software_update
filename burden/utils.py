import numpy as np
import pandas as pd
from flask import jsonify
from py2neo import Node, Graph, NodeMatcher
from burden.burden_calculator import burden_calculator
from burden.config import *
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from config import parthub_config

graph = Graph(parthub_config["serverUrl"], auth=("neo4j", "igem2024"), name="neo4j")
node_matcher = NodeMatcher(graph)

def read_basic_part_csv():
    part_types = ['promoter', 'RBS', 'CDS']
    res_dict = {}
    for part_type in part_types:
        try:
            df = pd.read_csv(f'./burden/data/{part_type.lower()}s.tsv', sep='\t', index_col=0, header=None)
        except:
            return None
        res_dict[part_type] = [{
            'name': df.index[i],
            'value': float(df.iloc[i, 0]),
            'seq': df.iloc[i, 1].upper()
        } for i in range(len(df))]
    return res_dict

def parse_basic_part(curPart: Node):
    registry_type = curPart['type']
    part_type = ''
    if registry_type == 'Promoter' or registry_type == 'Regulatory':
        part_type = 'promoter'
    elif registry_type == 'RBS':
        part_type = 'RBS'
    elif registry_type == 'Coding' or registry_type == 'Reporter':
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
    common_parts = read_basic_part_csv()
    if len(curPart['deep_subparts']) > 0:
        for subpart_num in curPart['deep_subparts']:
            if subpart_num.startswith('BBa_B003'):
                for rbs in common_parts['RBS']:
                    if rbs['name'] == subpart_num:
                        basic_parts.append({'type': 'RBS', 'info': {
                            'name': rbs['name'],
                            'seq': rbs['seq']
                        }})
                        break
                continue
            subpart = node_matcher.match("Part", number=subpart_num).first()
            if subpart is None:
                continue
            basic_parts.extend(parse_basic_part(subpart))
    else:
        basic_parts.extend(parse_basic_part(curPart))
    basic_parts = [part for part in basic_parts if part is not None]
    return jsonify({'parts': basic_parts}), 200


def calc_burden(parts: list[dict], copy_number: float, use_prap: bool):
    common_parts = read_basic_part_csv()
    common_parts_map = {}
    for part_type in common_parts:
        for part in common_parts[part_type]:
            common_parts_map[part['seq']] = part['value']

    promoter = parts[0]['info']
    if promoter['seq'] in common_parts_map:
        prom_strength = common_parts_map[promoter['seq']]
    else:
        prom_strength = calc_promoter_strength(promoter['seq'], parts[1]['info']['seq'])
    if prom_strength is None:
        return jsonify({'message': 'Failed to calculate promoter strength'}), 400
    ret_values = [prom_strength]
    tl_units = []
    for i in range(1, len(parts), 2):
        rbs = parts[i]['info']
        cds = parts[i + 1]['info']['seq'].upper()
        if rbs['seq'] in common_parts_map:
            rbs_strength = common_parts_map[rbs['seq']]
        else:
            rbs_strength = calc_rbs_strength(rbs['seq'], cds, use_prap)
        if rbs_strength is None:
            return jsonify({'message': 'Failed to calculate RBS strength'}), 400
        ret_values.append(rbs_strength)
        if len(cds) < 9 or len(cds) % 3 != 0 or cds[:3] != START_CODON or cds[-3:] not in STOP_CODONS:
            return jsonify({'message': 'Invalid CDS sequence'}), 400
        len_aa = len(cds) // 3 - 1
        if cds[-6:-3] in STOP_CODONS:
            len_aa -= 1
        ret_values.append(len_aa)
        tl_units.append((rbs_strength, len_aa, cds))
    return jsonify({
        'result': burden_calculator(copy_number, prom_strength, tl_units),
        'values': ret_values
    }), 200

from burden.promoter_calculator.wrapper import promoter_calculator

def calc_promoter_strength(prom_seq: str, rbs_seq: str):
    seq = (PROMOTER_UPSTREAM_SEQ + prom_seq + PROMOTER_RBS_SCAR + rbs_seq + RBS_CDS_SCAR).upper()
    output = promoter_calculator(seq)
    if len(output) == 0:
        return None
    return output[0]['Tx_rate'] * K_prom + B_prom


from burden.rbs_calculator.utils import run_rbs_predictor

def calc_rbs_strength(rbs_seq: str, cds: str, use_prap: bool):
    if use_prap:
        rbs_seq = (PRAP_RBS_PRE_SEQ + rbs_seq + PRAP_RBS_CDS_SEQ).upper()
    else:
        rbs_seq = (PROMOTER_RBS_SCAR + rbs_seq + RBS_CDS_SCAR).upper()
    post_seq = cds.upper()
    res = run_rbs_predictor('', post_seq, rbs_seq)
    return K_rbs * np.exp(-b_rbs * res.dG_total_list[0])