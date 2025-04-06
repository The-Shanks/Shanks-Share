from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO, send
import os
import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected users
connected_users = set()
app.secret_key = 'your_secret_key'

# SocketIO Events
@socketio.on('connect')
def handle_connect():
    connected_users.add(request.sid)
    send({'user': 'System', 'message': f'A new user connected. Total users: {len(connected_users)}'}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    connected_users.discard(request.sid)
    send({'user': 'System', 'message': f'A user disconnected. Total users: {len(connected_users)}'}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    if 'message' in data and data['message'].strip():
        timestamp = datetime.datetime.now().strftime('%H:%M')
        message_data = {
            'user': data.get('user', 'Anonymous'),
            'message': data['message'],
            'timestamp': timestamp
        }
        send(message_data, broadcast=True)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'STORAGE')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
def get_files():
    # List files in the STORAGE folder
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        offset = int(request.form.get('offset', 0))
        total_size = int(request.form.get('totalSize', 0))
        
        # Open file in append mode if offset > 0, otherwise create new file
        mode = 'ab' if offset > 0 else 'wb'
        with open(file_path, mode) as f:
            while True:
                chunk = file.stream.read(1024 * 1024)  # Read 1MB chunks
                if not chunk:
                    break
                f.write(chunk)
        
        # If this was the last chunk, return success
        if offset + file.stream.tell() >= total_size:
            return jsonify({"success": f"File '{file.filename}' uploaded successfully!"})
        else:
            return jsonify({"status": "chunk_uploaded"})
            
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"success": f"File '{filename}' deleted successfully!"})
    return jsonify({"error": f"File '{filename}' not found!"}), 404

if __name__ == '__main__':
    # Get the local IP address
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    
    print(f" * Running on http://{local_ip}:5000")
    print(" * Access this from other devices on your network using the above IP")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
