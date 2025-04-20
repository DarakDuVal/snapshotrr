from flask import Flask, request, jsonify
from db import init_db, save_backup, restore_backup, list_files, create_user
from auth import require_auth
import os

app = Flask(__name__)
init_db()

@app.route('/backup', methods=['POST'])
@require_auth
def backup():
    file_path = request.json.get('file_path')
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    save_backup(file_path)
    return jsonify({"status": "backup successful"}), 200

@app.route('/restore', methods=['POST'])
@require_auth
def restore():
    file_name = request.json.get('file_name')
    restored_path = restore_backup(file_name)
    return jsonify({"status": "restored", "path": restored_path}), 200

@app.route('/list', methods=['GET'])
@require_auth
def list_backups():
    return jsonify(list_files())

@app.route('/create-user', methods=['POST'])
@require_auth
def create_user_route():
    data = request.json
    create_user(data['username'], data['password'])
    return jsonify({'status': 'user created'})
