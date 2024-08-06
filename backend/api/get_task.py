from flask import Blueprint, request, jsonify
from .models import db, Users, Tasks
import random

get_task_bp = Blueprint('get_task', __name__)


@get_task_bp.route('/api/task/<user_id>', methods=['GET'])
def get_task(user_id):
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 404

    # Найти пользователя с данным user_id
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Найти все задания, которые не назначены ни одному пользователю
    task = Tasks.query.filter_by(id=user.task_id).first()
    if not task:
        return jsonify({}), 404
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Something went wrong: {str(e)}'}), 500

    return jsonify({
        'task_id': task.id,
        'text': task.text,
        'passed': task.passed,
        'file_id': task.file_id
    }), 200
