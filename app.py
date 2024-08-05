from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os
import random
import string
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Directory for log files and uploads
LOG_DIR = 'logs'
UPLOAD_DIR = 'static/uploads'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Load existing messages for a chat group
def load_messages(group):
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(LOG_DIR, f'{group}_{today}.txt')
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            messages = file.readlines()
        return [message.strip() for message in messages]
    return []

# Save a new message for a chat group
def save_message(group, username, message):
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(LOG_DIR, f'{group}_{today}.txt')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(log_file, 'a') as file:
            file.write(f'{timestamp} - {username}: {message}\n')
    except Exception as e:
        print(f'Error writing to log file: {e}')

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('choose_username'))
    return render_template('index.html', username=session['username'])

@app.route('/choose_username')
def choose_username():
    return render_template('choose_username.html')

@app.route('/set_username', methods=['POST'])
def set_username():
    username = request.json.get('username')
    if username:
        session['username'] = username
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

@app.route('/reset_username', methods=['POST'])
def reset_username():
    session.pop('username', None)
    return jsonify({'status': 'success'})

@app.route('/chat/<group>')
def chat(group):
    if 'username' not in session:
        return redirect(url_for('choose_username'))
    return render_template('index.html', username=session['username'], group=group)

@app.route('/send_message/<group>', methods=['POST'])
def send_message(group):
    username = session.get('username')
    message = request.form.get('message')
    file = request.files.get('file')

    if username and message:
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_DIR, filename)
            file.save(filepath)
            message += f' (File: <a href="/{filepath}">{filename}</a>)'
        save_message(group, username, message)
        return redirect(url_for('chat', group=group))
    return jsonify({'status': 'error'}), 400

@app.route('/get_messages/<group>', methods=['GET'])
def get_messages(group):
    messages = load_messages(group)
    return jsonify(messages)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
