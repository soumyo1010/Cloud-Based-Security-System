import os
from flask import Flask, request, jsonify, send_file
import mysql.connector
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection setup
db = mysql.connector.connect(
    host='database-1.ct6o6ggosi8e.eu-north-1.rds.amazonaws.com',
    user='Soumyo',
    password='Mummum10*',
    database='security_system'
)
cursor = db.cursor()

# Ensure 'local_uploads' folder exists
if not os.path.exists('local_uploads'):
    os.makedirs('local_uploads')

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", (username, password))
        user = cursor.fetchone()

        if user:
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# Endpoint to upload videos
@app.route('/upload', methods=['POST'])
def local_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file locally
    file_path = os.path.join('local_uploads', file.filename)
    file.save(file_path)

    # Insert video details into the database
    try:
        cursor.execute("INSERT INTO videos (file_name, file_path) VALUES (%s, %s)", 
                       (file.filename, file_path))
        db.commit()

        # Log the upload event
        cursor.execute("INSERT INTO logs (event_type, description, timestamp) VALUES (%s, %s, %s)",
                       ('video_uploaded', f'Video {file.filename} uploaded', datetime.now()))
        db.commit()

        return jsonify({'message': '🎉 Video uploaded successfully!'}), 200
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# Endpoint to fetch all videos
@app.route('/videos', methods=['GET'])
def get_videos():
    try:
        cursor.execute("SELECT * FROM videos")
        videos = cursor.fetchall()
        video_list = [{'file_name': video[1], 'file_path': video[2]} for video in videos]
        return jsonify(video_list), 200
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# Endpoint to fetch all logs
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        cursor.execute("SELECT * FROM logs")
        logs = cursor.fetchall()
        log_list = [{'event_type': log[1], 'description': log[2], 'timestamp': log[3]} for log in logs]
        return jsonify(log_list), 200
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

# Endpoint to download a video
@app.route('/download/<filename>', methods=['GET'])
def download_video(filename):
    try:
        file_path = os.path.join('local_uploads', filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)