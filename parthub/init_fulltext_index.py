"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : init_fulltext_index.py
@Author : Assistant
@Time : 2026/05/01
"""
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from py2neo import Graph
from config import parthub_config

graph = Graph(parthub_config["serverUrl"], auth=("neo4j", "igem2024"), name="neo4j")

INDEX_NAME = "partSearch"


def create_fulltext_index():
    # Check if index already exists
    query = f"SHOW INDEXES YIELD name, type WHERE name = '{INDEX_NAME}' AND type = 'FULLTEXT'"
    result = graph.run(query).data()

    if result:
        print(f"Full-text index '{INDEX_NAME}' already exists.")
        return

    # Neo4j 5.x native syntax for creating full-text index
    query = f"""
    CREATE FULLTEXT INDEX `{INDEX_NAME}` FOR (n:Part) ON EACH [n.number, n.name, n.contents, n.designer, n.team]
    OPTIONS {{
      indexConfig: {{
        `fulltext.analyzer`: 'standard'
      }}
    }}
    """
    graph.run(query)
    print(f"Full-text index '{INDEX_NAME}' created successfully.")


def drop_fulltext_index():
    query = f"SHOW INDEXES YIELD name, type WHERE name = '{INDEX_NAME}' AND type = 'FULLTEXT'"
    result = graph.run(query).data()

    if not result:
        print(f"Full-text index '{INDEX_NAME}' does not exist.")
        return

    # Neo4j 5.x native syntax for dropping index
    query = f"DROP INDEX `{INDEX_NAME}`"
    graph.run(query)
    print(f"Full-text index '{INDEX_NAME}' dropped.")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Manage Neo4j full-text index for PartHub")
    parser.add_argument("action", choices=["create", "drop"], default="create", nargs="?",
                        help="Action to perform: create or drop the index")
    args = parser.parse_args()

    if args.action == "create":
        create_fulltext_index()
    else:
        drop_fulltext_index()
