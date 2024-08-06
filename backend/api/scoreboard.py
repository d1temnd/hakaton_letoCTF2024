from flask import Blueprint, request, jsonify
from .models import db, Users

scoreboard_bp = Blueprint('scoreboard', __name__)


@scoreboard_bp.route('/api/scoreboard', methods=['GET'])
def get_scoreboard():
    # Получаем список всех пользователей, отсортированных по очкам в порядке убывания
    users = Users.query.order_by(Users.score.desc()).all()

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