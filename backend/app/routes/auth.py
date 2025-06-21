from flask import request, jsonify
from models.user import User
from flask import Blueprint
from .create_engine_sessions import create_engine_and_sessions
import datetime
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import pytz
import bcrypt
auth_bp = Blueprint('auth', __name__)

jwt = JWTManager()  

@auth_bp.route('/register', methods=['POST'])
def add_user():
    data = request.json
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    new_user = User(full_name=data['full_name'], email=data['email'], hashed_password=hashed_password.decode('utf-8'))
    try:
        session = create_engine_and_sessions()
        user = session.query(User).filter_by(email=data['email']).first()
        if user:
            return jsonify({"error": "User already exists!"}), 409
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
            return jsonify({"error": "Invalid email"}), 401
        
        if user and user.token:
            return jsonify({"error": "User already logged in"}), 409
       
        if user and bcrypt.checkpw(data['password'].encode('utf-8'),  user.hashed_password.encode('utf-8')):        
            timezone = pytz.timezone('Europe/Bucharest')
            now_utc = datetime.datetime.now(timezone)
            access_token = create_access_token(identity=user.email, expires_delta=datetime.timedelta(minutes=2))
            refresh_token = create_refresh_token(identity=user.email)
            user.token = access_token
            user.token_expiration = now_utc + datetime.timedelta(minutes=50)
            session.commit()
            return jsonify({"token": access_token, "refresh_token": refresh_token}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401

    except Exception as e:
        
        return jsonify({"error": str(e)}), 501
    finally:
        session.close()

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        print("Request received at /logout")
        current_user = get_jwt_identity()
        session = create_engine_and_sessions()
        user = session.query(User).filter_by(email=current_user).first()
        user.token = None
        user.token_expiration = None
        session.commit()
        return jsonify({"message": "User logged out"}), 200
    except Exception as e:
        return jsonify({"error": 'Server Error!'}), 501
    finally:
        session.close()

@auth_bp.route('/videoDownload', methods=['GET'])
@jwt_required()
def videoDownload():
    return jsonify({"message": "Token still valid"}), 200

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify(msg="Token has expired"), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()  
    new_access_token = create_access_token(identity=identity)
    session = create_engine_and_sessions()
    user = session.query(User).filter_by(email=identity).first()
    user.token = new_access_token
    return jsonify(access_token=new_access_token), 200
       