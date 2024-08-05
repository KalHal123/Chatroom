from flask import Flask, request, jsonify, render_template, session
import os
import random
import string
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# File to store messages
MESSAGE_FILE = 'messages.txt'

# Helper function to generate a random username
def generate_username():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Load existing messages
def load_messages():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, 'r') as file:
            messages = file.readlines()
        return [message.strip() for message in messages]
    return []

# Save a new message
def save_message(username, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(MESSAGE_FILE, 'a') as file:
        file.write(f'{timestamp} - {username}: {message}\n')

@app.route('/')
def index():
    if 'username' not in session:
        session['username'] = generate_username()  # Generate a random username if not set
    return render_template('index.html', username=session['username'])

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
