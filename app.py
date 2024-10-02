"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : utils.py
@Author : Hongchen Chen
@Time : 2024/08/31 15:34:00
"""

import os.path

from flask import Flask, render_template, request, jsonify, send_file
from flask_compress import Compress
from os import path
from werkzeug.utils import secure_filename

import config
from parthub.utils import parthub_search, create_parthub_seq_file, get_part_id
from similarity.utils import query_similarity, parse_part_file, add_new_part
from burden.utils import read_basic_part_csv, get_basic_parts, calc_burden

parthub_config = config.parthub_config
parthub_config["serverUrl"] = 'bolt://localhost:7687'
template_folder = path.abspath('webUI/template')
static_folder = path.abspath('webUI/static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, static_url_path='')
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
Compress(app)


# for web pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/burden')
def burden():
    return render_template('burden.html')

@app.route('/parthub')
def parthub():
    return render_template('parthub.html')


@app.route('/parts')
def parts():
    return render_template('parts.html')


@app.route('/treemap')
def treeMap():
    return render_template('treeMap.html')


# for apis
@app.route('/api/burden/get_basic_part_info', methods=['GET'])
def handle_get_basic_part_info():
    res = read_basic_part_csv()
    if res is None:
        app.logger.warning('Failed to read basic part info')
        return jsonify({"message": "Failed to read basic part info"}), 500
    return jsonify({"result": res}), 200


@app.route('/api/burden/get_basic_parts', methods=['POST'])
def handle_get_basic_parts():
    data = request.json
    if not data or not data.get('number'):
        app.logger.warning('Missing data')
        return jsonify({"message": "Missing data"}), 400
    part_num = data.get('number')
    return get_basic_parts(part_num)

@app.route('/api/burden/calculate', methods=['POST'])
def handle_calc_burden():
    data = request.json
    if not data or not data.get('parts') or not data.get('copy_number') or not data.get('use_prap'):
        app.logger.warning('Missing data')
        return jsonify({"message": "Missing data"}), 400
    res = calc_burden(data.get('parts'), float(data.get('copy_number')), data.get('use_prap') == 'true')
    return res
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def handle_upload_part_file(request, part_type):
    if 'file' not in request.files:
        app.logger.warning('Missing file')
        return jsonify({"message": "Missing file"}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        ret = parse_part_file(file_path, part_type)
        os.remove(file_path)
        return ret
    else:
        app.logger.warning('Invalid file type')
        return jsonify({"message": "Invalid file type"}), 400

@app.route('/api/upload_part_file/promoter', methods=['POST'])
def handle_upload_promoter_file():
    return handle_upload_part_file(request, 'promoter')

@app.route('/api/upload_part_file/RBS', methods=['POST'])
def handle_upload_rbs_file():
    return handle_upload_part_file(request, 'RBS')

@app.route('/api/upload_part_file/CDS', methods=['POST'])
def handle_upload_cds_file():
    return handle_upload_part_file(request, 'CDS')

@app.route('/api/upload_part_file/default', methods=['POST'])
def handle_upload_default_file():
    return handle_upload_part_file(request, 'default')


@app.route('/api/parthub/add_new_part', methods=['POST'])
def handle_add_new_part():
    data = request.json
    if not data or not data.get('type') or not data.get('seq'):
        app.logger.warning('Missing data')
        return jsonify({"message": "Missing data"}), 400
    part_type = data.get('type')
    seq = data.get('seq')
    return add_new_part(part_type, seq)

@app.route('/api/parthub/search', methods=['POST'])
def handle_parthub_search():
    data = request.json
    if not data or not data.get('partHubQuery') or not data.get('partHubType'):
        app.logger.warning('Missing query or type')
        return jsonify({"message": "Missing query or type"}), 400
    query = data.get('partHubQuery')
    search_type = data.get('partHubType')
    return parthub_search(query, search_type)


@app.route('/api/parthub/config', methods=['POST'])
def handle_parthub_config():
    data = request.json
    if not data or not data.get('curPart'):
        app.logger.warning('Missing curPart')
        return jsonify({"message": "Missing curPart"}), 400
    return jsonify({'id': get_part_id(data.get('curPart')), 'config': parthub_config}), 200


@app.route('/api/parthub/query_similarity', methods=['POST'])
def handle_query_similarity():
    data = request.json
    if not data or not data.get('curPart'):
        app.logger.warning('Missing curPart')
        return jsonify({"message": "Missing curPart"}), 400
    curPart = data.get('curPart')
    res = query_similarity(curPart)
    if res is None:
        return jsonify({"message": "Similarity query failed"}), 500
    return jsonify({"result": res}), 200


# for file download
@app.route('/download/<filename>')
def handle_download(filename):
    filepath = os.path.join('./results', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)


@app.route('/seq/download/<part_id>')
def handle_seq_download(part_id):
    filepath = create_parthub_seq_file(part_id)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    print('Starting Flask server...')
    app.run(host='0.0.0.0', port=5000)
    print('Flask server started!')