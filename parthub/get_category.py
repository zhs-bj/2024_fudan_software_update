"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : get_category.py
@Author : Hongchen Chen
@Time : 2024/9/15 23:09
"""
import numpy as np
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm

def Findall(v, tag):
    return [i for i in v.iter(tag)]
def Find(v, tag):
    ret = Findall(v, tag)
    return ret[0] if len(ret) > 0 else None

for yr in range(2004, 2024):
    print(f'Getting {yr}...', flush=True)
    data = pd.read_csv(f'../parthub/collections/{yr}collection.csv', index_col=0)
    data.loc[:, 'category'] = ''
    data.loc[:, 'using_parts_deep'] = ''
    for part in tqdm(data.index):
        try:
            x = requests.get(f'https://parts.igem.org/cgi/xml/part.cgi?part={part}')
            assert x.status_code == 200
            x = ET.fromstring(x.text)
            data.loc[part, 'category'] = ' '.join([cat.text.strip()
                                            for cat in Findall(Find(x, 'categories'),'category')])
            data.loc[part, 'using_parts_deep'] = ' '.join([Find(subpart, 'part_name').text.strip()
                                            for subpart in Findall(Find(x, 'deep_subparts'),'subpart')])
        except:
            continue
    data.to_csv(f'../parthub/new_collections/{yr}collection.csv')