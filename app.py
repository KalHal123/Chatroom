from flask import Flask, request, jsonify, render_template
import os
import random
import string

app = Flask(__name__)

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
    with open(MESSAGE_FILE, 'a') as file:
        file.write(f'{username}: {message}\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    username = data.get('username')
    message = data.get('message')
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
