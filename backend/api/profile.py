from flask import Blueprint, request, jsonify
from .models import db, Users

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/api/profile/<user_id>', methods=['GET'])
def profile(user_id):
    # Найти пользователя по user_id
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Получить информацию о пользователе
    username = user.username
    score = user.score

    # Найти позицию пользователя в общем рейтинге
    # Сначала получаем всех пользователей, отсортированных по score в порядке убывания
    users = Users.query.order_by(Users.score.desc()).all()

    # Определяем позицию пользователя
    position = next((index + 1 for index, u in enumerate(users) if u.user_id == user_id), None)

    if position is None:
        return jsonify({'error': 'Could not determine position'}), 500

    # Формируем ответ
    response = {
        'username': username,
        'score': score,
        'position': position,
        'task_id': user.task_id
    }

    return jsonify(response), 200
