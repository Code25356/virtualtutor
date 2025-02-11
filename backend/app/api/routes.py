from flask import jsonify
from . import api

@api.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})