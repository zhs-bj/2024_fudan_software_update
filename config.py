"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : utils.py
@Author : Hongchen Chen
@Time : 2024/08/31 15:46:50
"""

import os

parthub_config = {
    "serverUrl": os.environ.get('SERVER_URL'),
    "serverUser": os.environ.get('SERVER_USER'),
    "serverPassword": os.environ.get('SERVER_PASSWORD')
}

UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'gb', 'fa', 'fasta'}
