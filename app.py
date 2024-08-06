from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'oawduhamoiuhiuh&12391864-daohd9184'  # Change this to a random secret key

# Directory for log files
LOG_DIR = 'logs'
UPLOAD_DIR = 'static/uploads'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Save a new message
def save_message(group, username, message):
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(LOG_DIR, f'{group}_{today}.txt')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as file:
        file.write(f'{timestamp} - {username}: {message}\n')

@app.route('/')
def index():
    if 'username' not in session:
        return render_template('choose_username.html')
    return render_template('index.html', username=session['username'], group='general')

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

@app.route('/send_message/<group>', methods=['POST'])
def send_message(group):
    username = session.get('username')
    message = request.form.get('message')
    file = request.files.get('file')

    if username and (message or file):
        if message:
            save_message(group, username, message)
        if file:
            filename = file.filename
            file_path = os.path.join(UPLOAD_DIR, filename)
            file.save(file_path)
        return redirect(url_for('chat', group=group))
    return jsonify({'status': 'error'}), 400

@app.route('/chat/<group>')
def chat(group):
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('index.html', username=session['username'], group=group)

@app.route('/get_messages/<group>', methods=['GET'])
def get_messages(group):
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(LOG_DIR, f'{group}_{today}.txt')
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            messages = file.readlines()
        return jsonify([message.strip() for message in messages])
    return jsonify([])

@app.route('/impress')
def impress():
    return render_template('impress.html')

@app.route('/license')
def license():
    return render_template('license.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
