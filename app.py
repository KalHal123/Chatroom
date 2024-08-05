from flask import Flask, request, jsonify, render_template, session
import os
import random
import string
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Directory for log files
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Load existing messages
def load_messages():
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(LOG_DIR, f'{today}.txt')
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            messages = file.readlines()
        return [message.strip() for message in messages]
    return []

# Save a new message
def save_message(username, message):
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(LOG_DIR, f'{today}.txt')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(log_file, 'a') as file:
            file.write(f'{timestamp} - {username}: {message}\n')
    except Exception as e:
        print(f'Error writing to log file: {e}')

@app.route('/')
def index():
    if 'username' not in session:
        return render_template('choose_username.html')
    return render_template('index.html', username=session['username'])

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

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    username = session.get('username')
    if username and message:
        save_message(username, message)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = load_messages()
    return jsonify(messages)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
