from flask import Blueprint, request, jsonify
from .models import db, Users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth', methods=['POST'])
def auth():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request: No JSON data provided'}), 404

    user_id = data.get('user_id')
    username = data.get('username')
    task_id = data.get('task_id', 0)

    if not user_id or not username:
        return jsonify({'error': 'Missing user_id or username'}), 404

    if Users.query.filter_by(user_id=user_id).first():
        return jsonify({'message': 'User already registered'}), 200

    try:
        new_user = Users(user_id=user_id, username=username, task_id=task_id)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Something went wrong: {str(e)}'}), 404
