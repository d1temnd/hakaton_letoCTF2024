from flask import Blueprint, request, jsonify
from .models import db, User

scoreboard_bp = Blueprint('scoreboard', __name__)


@scoreboard_bp.route('/api/scoreboard', methods=['GET'])
def get_scoreboard():
    # Получаем список всех пользователей, отсортированных по очкам в порядке убывания
    users = User.query.order_by(User.score.desc()).all()

    # Формируем ответ
    response = [
        {
            'username': user.username,
            'user_id': user.user_id,
            'score': user.score
        }
        for user in users
    ]

    return jsonify(response)