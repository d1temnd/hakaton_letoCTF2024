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
    available_tasks = Tasks.query.filter(
        ~Tasks.id.in_(Users.query.with_entities(Users.task_id).filter(Users.task_id.isnot(None)))).all()

    if not available_tasks:
        # return jsonify({'error': 'No available tasks'}), 404
        return jsonify({}), 404
    # Выбрать случайное задание из доступных
    task = random.choice(available_tasks)

    # Проверить, сколько пользователей уже имеют это задание
    assigned_users = Users.query.filter_by(task_id=task.id).all()
    if len(assigned_users) >= 2:
        return jsonify({'error': 'Task already assigned to two users'}), 404

    # Найти случайного пользователя с task_id = None и который не является текущим пользователем
    random_user = Users.query.filter(Users.task_id.is_(None), Users.id != user.id).order_by(func.random()).first()
    if not random_user:
        return jsonify({'error': 'No available users to assign task'}), 404

    # Назначить задание пользователю и другому случайному пользователю
    if user.task_id is None:
        user.task_id = task.id
    if random_user.task_id is None:
        random_user.task_id = task.id

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Something went wrong: {str(e)}'}), 500

    # Вернуть информацию о задании
    return jsonify({
        'task_id': task.id,
        'text': task.text,
        'passed': task.passed,
        'file_id': task.file_id
    }), 200
