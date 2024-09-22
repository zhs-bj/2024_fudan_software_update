import os.path

from flask import Flask, render_template, request, jsonify, send_file
from flask_compress import Compress
from os import path
from werkzeug.utils import secure_filename

import config
from parthub.utils import parthub_search, create_parthub_seq_file, get_part_id
from similarity.utils import query_similarity
from burden.utils import read_basic_part_csv, parse_gb_file

UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'gb'}
parthub_config = config.parthub_config
template_folder = path.abspath('webUI/template')
static_folder = path.abspath('webUI/static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    return read_basic_part_csv()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/burden/upload_genbank_file', methods=['POST'])
# handle uploaded file in genbank format using Biopython
def handle_upload_genbank_file():
    if 'file' not in request.files:
        app.logger.warning('Missing file')
        return jsonify({"message": "Missing file"}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(parse_gb_file(filename)), 200
    else:
        app.logger.warning('Invalid file type')
        return jsonify({"message": "Invalid file type"}), 400

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
    app.run(debug=True, host='0.0.0.0', port=5000) # TO BE MODIFIED
    print('Flask server started!')