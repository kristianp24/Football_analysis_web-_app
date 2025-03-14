from flask import request, jsonify
from models.user import User
from flask import Blueprint
from .create_engine_sessions import create_engine_and_sessions
import datetime
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import pytz
import bcrypt
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def add_user():
    data = request.json
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    new_user = User(full_name=data['full_name'], email=data['email'], hashed_password=hashed_password.decode('utf-8'))
    try:
        session = create_engine_and_sessions()
        user = session.query(User).filter_by(email=data['email']).first()
        if user:
            return jsonify({"error": "User already exists"}), 409
        session.add(new_user)
        session.commit()

        return jsonify({"message":"User added with success!!"}), 201

    except Exception as e:
        session.rollback()  
        return jsonify({"error": str(e)}), 501
    finally:
        session.close()  

@auth_bp.route('/login', methods=['POST'])
def fetch_user():
    data = request.json
    try:
        session = create_engine_and_sessions()
        user = session.query(User).filter_by(email=data['email']).first()
        if not user:
            return jsonify({"error": "Invalid email or password"}), 404
        if user.token:
            return jsonify({"error": "User already logged in"}), 401
       
        if user and bcrypt.checkpw(data['password'].encode('utf-8'),  user.hashed_password.encode('utf-8')):        
            timezone = pytz.timezone('Europe/Bucharest')
            now_utc = datetime.datetime.now(timezone)
            access_token = create_access_token(identity=user.email)
            user.token = access_token
            user.token_expiration = now_utc + datetime.timedelta(hours=1)
            session.commit()
            return jsonify({"token": access_token}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        
        return jsonify({"error": str(e)}), 501
    finally:
        session.close()

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    try:
        current_user = get_jwt_identity()
        session = create_engine_and_sessions()
        user = session.query(User).filter_by(email=current_user).first()
        if not user.token:
            session.close()
            return jsonify({"error": "User is not logged in"}), 401
        if user.token_expiration < datetime.datetime.now():
            session.close()
            return jsonify({"error": "Token expired"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 501
    finally:
        session.close()
        return jsonify(logged_in_as=current_user), 200
       

