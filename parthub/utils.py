"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : utils.py
@Author : Zhiyue Chen
@Time : 2023/9/3 13:47
"""
import os
from operator import itemgetter
from typing import Any

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from flask import jsonify, Response
from py2neo import Node, Graph, NodeMatcher
import re

graph = Graph("bolt://parthub:7687", auth=("neo4j", "igem2024"), name="neo4j")
node_matcher = NodeMatcher(graph)


def content_match(node: Node, search_key: str) -> str:
    """
    :param node: selected node
    :param search_key: inputted search keyword
    :return: content that matches search keyword
    """
    content = dict(node)['contents']
    content_lst = re.split(' ', content)
    for i in range(len(content_lst)):
        if search_key in content_lst[i]:
            r = 20
            if i >= r and i + r < len(content_lst) - 1:
                return ' '.join(content_lst[i - r:i + r])
            elif i >= r and i + r > len(content_lst) - 1:
                return ' '.join(content_lst[i - r:len(content_lst) - 1])
            elif i < r and i + r < len(content_lst) - 1:
                return ' '.join(content_lst[0:i + r])
            else:
                return ' '.join(content_lst[0:len(content_lst) - 1])


def search_node(search_key: str, search_type: str) -> list[dict[str | Any, str | Any]] | None:
    """
    :param search_key: inputted search keyword
    :param search_type: type of the search keyword
    :return: a list contains searched dict format of nodes
    """
    node_dic_list = []
    if search_type == 'sequence':
        search_key = search_key.lower()
        key_inverse = search_key.replace("a", "t").replace("t", "a").replace("c", "g").replace("g", "c")
        sequence_query = "_.sequence =~ '(?i).*key.*' OR _.sequence =~ '(?i).*inverse.*'"
        sequence_query_temp = re.sub('key', search_key.lower(), sequence_query)
        sequence_query = re.sub('inverse', key_inverse, sequence_query_temp)
        nodes = list(node_matcher.match("Part").where(sequence_query))
    else:
        query = "_.type =~ '(?i).*key.*'"
        query_temp = re.sub('type', search_type, query)
        query = re.sub('key', search_key, query_temp)
        nodes = list(node_matcher.match("Part").where(query))
    if not nodes:
        return
    keys_required = ['year', 'team', 'designer', 'type', 'number', 'name', 'contents', 'cites', 'twins_num', 'length',
                     'isfavorite', 'released', 'date', 'url', 'pagerank', 'community']
    for node in nodes:
        node_dic = dict(node)
        node_dic = {key: value for key, value in node_dic.items() if key in keys_required}
        if search_type == 'contents':
            node_dic['matchedContents'] = content_match(node, search_key)
            node_dic.pop('contents', None)
            node_dic_list.append(node_dic)
        elif search_type == 'name':
            node_dic['matchedContents'] = node_dic['contents'][:200]
            node_dic.pop('contents', None)
            node_dic_list.append(node_dic)
        else:
            node_dic['matchedContents'] = node_dic['contents'][:200]
            node_dic.pop('contents', None)
            node_dic_list.append(node_dic)
    return node_dic_list


def multiple_search(kwd_list: list[str], search_type: str, flag: str) -> None | list[dict] | list[Any] | Any:
    """
    :param kwd_list: list contains all inputted search keywords for multiple search
    :param search_type: type of the search keyword
    :param flag: logical flag, like 'AND'
    :return: a list contains searched dict format of nodes
    """
    if len(kwd_list) < 2:
        return
    res = []
    if flag == 'AND':
        res = search_node(kwd_list[0], search_type)
        num_list = get_num_list(res)
        for kwd in kwd_list[1:]:
            if res:
                res = [i for i in search_node(kwd, search_type) if i.get('number') in num_list]
                num_list = get_num_list(res)
            else:
                return
    else:
        num_list = []
        for kwd in kwd_list:
            res = res + [i for i in search_node(kwd, search_type) if i.get('number') not in num_list]
            num_list = get_num_list(res)
    return res


def get_num_list(node_dic_list: list[dict]) -> list[str]:
    """
    :param node_dic_list: list contains searched dict format of nodes
    :return: a list contains numbers of each node
    """
    return [i.get('number') for i in node_dic_list]


def sort_node(node_dic_lst: list[dict]):
    """
    :param node_dic_lst: list contains searched dict format of nodes
    :return: sorted list contains searched dict format of nodes
    """
    sorted_node_dic_lst = sorted(node_dic_lst, key=itemgetter('pagerank'), reverse=True)
    seen_communities = set()
    unique_community_list = []
    else_list = []
    for item in sorted_node_dic_lst:
        if item["community"] not in seen_communities:
            unique_community_list.append(item)
            seen_communities.add(item["community"])
        else:
            else_list.append(item)
    return unique_community_list + else_list


def parthub_search(search_key: str, search_type: str) -> tuple[Response, int]:
    if ' AND ' in search_key:
        kwd_list = search_key.split(' AND ')
        all_res = multiple_search(kwd_list, search_type, 'AND')
    elif ' OR ' in search_key:
        kwd_list = search_key.split(' OR ')
        all_res = multiple_search(kwd_list, search_type, 'OR')
    else:
        all_res = search_node(search_key, search_type)
    if all_res:
        return jsonify(sort_node(all_res)), 200
    else:
        return jsonify({'message': 'No search result found'}), 200


def init_create() -> None:
    if not os.path.exists(r'./parthub'):
        os.makedirs(r'./parthub')


def create_parthub_seq_file(part_id: str) -> str:
    """
    :param part_id: the id of the part, like BBa_K3606003
    :return: path of the sequence file in GeneBank format
    """
    init_create()
    filename = part_id + '.gb'
    query = """
    MATCH (p:Part {number: 'part_id'})
    RETURN p.sequence;
    """
    query = re.sub('part_id', part_id, query)
    sequence = str(graph.run(query).evaluate())
    seq_record = SeqRecord(Seq(sequence), id=part_id)
    seq_record.annotations["molecule_type"] = "DNA"
    with open(os.path.join(r'./parthub', filename), 'w') as f:
        SeqIO.write(seq_record, f, "genbank")
    return os.path.join(r'./parthub', filename)


def get_part_id(name: str) -> str:
    """
    :param name: the id of the part, like BBa_K3606003
    :return: part id in neo4j database
    """
    query = """
        MATCH (p:Part {number: 'part_id'})
        RETURN ID(p);
        """
    query = re.sub('part_id', name, query)
    part_id = str(graph.run(query).evaluate())
    return part_id
