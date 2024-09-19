import os.path

from flask import Flask, render_template, request, jsonify, send_file
from flask_compress import Compress
from os import path

import config
from parthub.utils import parthub_search, create_parthub_seq_file, get_part_id
from similarity.utils import query_similarity

parthub_config = config.parthub_config
template_folder = path.abspath('webUI/template')
static_folder = path.abspath('webUI/static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, static_url_path='')
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
@app.route('/api/burden', methods=['POST'])
def handle_burden_query():
    data = request.json
    return None

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


# @app.route('/api/test/connection')
# def handle_test_connection():
#     return test_connection()



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
    app.run(debug=True, host='0.0.0.0', port=5000) # TO BE MODIFIED
    print('Flask server started!')