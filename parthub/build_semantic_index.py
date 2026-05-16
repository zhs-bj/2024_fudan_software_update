#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Offline script to build semantic search index for all iGEM parts.
Run this once after setting up Neo4j, or whenever parts data changes.

Usage:
    python -m parthub.build_semantic_index
"""
from parthub.semantic_search import build_semantic_index

if __name__ == '__main__':
    build_semantic_index()
