from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .credentials import VIDEO_PATH
import os
from .email_sender import send_prediction_ready_email

video_bp = Blueprint('video_bp', __name__)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

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
        return jsonify({"message":"Video added with success!!"}), 200

@video_bp.route('/predictVideo', methods=['GET', 'POST'])
@jwt_required()
def get_video():
    user_email = get_jwt_identity()  
    from prediction import predict
    print('Starting prediction')
    is_predicted, data = predict(VIDEO_PATH, video_name)
    
    if is_predicted:
        is_email_sent = send_prediction_ready_email(user_email)
        if is_email_sent:
            return jsonify({"message":"Video predicted with success!!", "data": data}), 200
        else:
            return jsonify({"error": "Error sending email"}), 500
    else:
        return jsonify({"error": "Error in prediction"}), 500
    