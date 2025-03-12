from flask import Blueprint
from models.user import User
from flask import jsonify
from .create_engine_sessions import create_engine_and_sessions

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
