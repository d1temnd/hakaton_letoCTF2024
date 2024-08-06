from flask import Blueprint, request, jsonify
from .models import db, Users, Tasks
import random
import json

admin_start_game_bp = Blueprint('admin_start_game', __name__)


@admin_start_game_bp.route("/api/admin/start_game", methods=['GET', 'POST'])
def admin_start_game():
    # Найти пользователя с данным user_id
    users = Users.query.all()
    if not users:
        return jsonify({'error': 'User not found'}), 404

    # Перемешиваем список пользователей
    random.shuffle(users)

    # Создаем пары
    pairs = []
    for i in range(0, len(users), 2):
        pair = users[i:i + 2]
        if len(pair) == 2:
            pairs.append(pair)
    #
    # for pain in pairs:
    #     user1 = users[0]
    #     user2 = users[1]
    #     print(user2, user1['username'])
    #
    #     with open('words/task.json', encoding="utf-8") as f:
    #         data = json.load(f)
    #
    #     obj = random.choice(data["object"])
    #     selected_prop = random.choice(list(obj["prop"].keys()))
    #
    #     action = random.choice(data["action"])
    #     place = random.choice(data["place"])
    #     prop = random.choice(obj["prop"][selected_prop])
    #     obj = random.choice(obj["obj"])
    #
    #     text_task = f'''{user1['username']}, {user2['username']}:
    #         Действие: {action}.
    #         Объект: {prop} {obj}.
    #         Место: {place}.'''
    #     # Выводим пары
    #
    #     usertask = Tasks(text=text_task)
    #     db.session.commit()
    #     print(usertask)
    #
    # print(pairs)
    return jsonify({}), 200
