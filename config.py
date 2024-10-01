import os

parthub_config = {
    "serverUrl": os.environ.get('SERVER_URL'),
    "serverUser": os.environ.get('SERVER_USER'),
    "serverPassword": os.environ.get('SERVER_PASSWORD')
}

UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'gb', 'fa', 'fasta'}
