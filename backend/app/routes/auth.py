from flask import request, jsonify
from models.user import User
from flask import Blueprint
from .create_engine_sessions import create_engine_and_sessions

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def add_user():
    data = request.json
    user = User(full_name=data['full_name'], email=data['email'], hashed_password=data['hashed_password'])
    try:
        session = create_engine_and_sessions()
        session.add(user)
        session.commit()

        return jsonify({"message":"User added with success!!"}), 201

    except Exception as e:
        session.rollback()  
        return jsonify({"error": str(e)}), 501
    finally:
        session.close()  