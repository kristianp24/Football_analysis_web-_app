from flask import Blueprint, request, jsonify
from .credentials import VIDEO_PATH
import os

video_bp = Blueprint('video_bp', __name__)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'flv', 'mov'}

video_name = ''
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@video_bp.route('/saveVideo', methods=['POST'])
def add_video():
    global video_name 
    if 'video' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        file.save(os.path.join(VIDEO_PATH, file.filename))
        video_name = file.filename
        return jsonify({"message":"Video added with success!!"}), 201

@video_bp.route('/predictVideo', methods=['GET'])
def get_videos():
    video = os.listdir(VIDEO_PATH)
    from prediction import predict
    print('Starting prediction')
    is_predicted = predict(VIDEO_PATH, video_name)
    if is_predicted:
        return jsonify({"message":"Video predicted with success!!"}), 201
    else:
        return jsonify({"error": "Error in prediction"}), 500
    