from flask import Blueprint, request, jsonify
from .models import db, Users, Tasks

user_bp = Blueprint('user', __name__)


@user_bp.route("/api/users", methods=['POST', 'GET'])
def get_users():
    users = Users.query.order_by(Users.score.desc()).all()

    response = [
        {
            'username': user.username,
            'task_id': user.task_id

        }
        for user in users
    ]

    return jsonify(response)
