from flask import Blueprint, request, jsonify
from .models import db, Users, Tasks

pass_task_bp = Blueprint('pass_task', __name__)


@pass_task_bp.route('/api/pass_task', methods=['POST'])
def pass_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request: No JSON data provided'}), 404

    user_id = data.get('user_id')
    file_id = data.get('file_id')

    if not user_id or not file_id:
        return jsonify({'error': 'Missing user_id or file_id'}), 404

    # Найти пользователя по user_id
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Найти задание, назначенное этому пользователю
    task = Tasks.query.filter_by(id=user.task_id).first()
    if not task:
        return jsonify({'error': 'Task not found for the given user'}), 404

    # Обновить file_id в найденном задании
    task.file_id = file_id

    try:
        db.session.commit()
        return jsonify({'message': 'File ID updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
