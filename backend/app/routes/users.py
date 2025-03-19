from flask import Blueprint
from models.user import User
from flask import jsonify
from .create_engine_sessions import create_engine_and_sessions
from flask_jwt_extended import jwt_required, get_jwt_identity


users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        session = create_engine_and_sessions()

        users = session.query(User).all()
        users_list = [user.to_dict() for user in users]

        return jsonify({"users": users_list}), 200  
    
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        session.close()

@users_bp.route('/user/fullName', methods=['GET'])
@jwt_required()
def get_user_full_name():
    current_user = get_jwt_identity()
    try:
        session = create_engine_and_sessions()
        user_full_name = session.query(User.full_name).filter_by(email=current_user).scalar()
        if user_full_name:
            return jsonify({"full_name": user_full_name}), 200
        else:
            return jsonify({"error": 'Some error occured!'}), 500
    except Exception as e:
        return jsonify({'error': 'Error occured!'}), 500
    finally:
        session.close()

@users_bp.route('/user/email', methods=['GET'])
@jwt_required()
def get_user_email():
    try:
        email = get_jwt_identity()
        print(email, type(email))
        return jsonify({"email": email}), 200
    except Exception as e:
        return jsonify({"error": "Some error occured"}), 500
    
