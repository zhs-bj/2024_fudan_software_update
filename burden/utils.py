import numpy as np
import pandas as pd
from flask import jsonify

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

def parse_gb_file(filename):
    # Read genbank file and parse the features
    pass

def calc_burden(parts: list[dict]):
    pass