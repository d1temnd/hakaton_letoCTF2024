from flask import Blueprint, request, jsonify
from .models import db, Users, Tasks, Votes
import random
import json

admin_start_game_bp = Blueprint('admin_start_game', __name__)


@admin_start_game_bp.route("/api/admin/start_game", methods=['POST', 'GET'])
def admin_start_game():
    # Найти пользователя с данным user_id
    db.session.query(Tasks).delete()
    db.session.query(Votes).delete()
    db.session.commit()

    users = Users.query.all()
    if not users:
        return jsonify({'error': 'User not found'}), 404
    for user in users:
        user.task_id = None
    db.session.commit()
    random.shuffle(users)

    # Создаем пары
    pairs = []
    for i in range(0, len(users), 2):
        pair = users[i:i + 2]
        if len(pair) == 2:
            pairs.append(pair)
    for pair in pairs:
        user1 = pair[0]
        user2 = pair[1]

        with open('words/task.json', encoding="utf-8") as f:
            data = json.load(f)

        action = random.choice(data["action"])
        obj = random.choice(data["object"])
        place = random.choice(data["place"])
        topic = random.choice(data["topic"])

        templates = [
            f"{action} {obj} в {place}",
            f"В {place} {action} {topic}",
            f"{action} {obj}, обсуждая {topic}, в {place}"
        ]

        task = random.choice(templates)
        text_task = f'@{user1.username}, @{user2.username}:\n{task}'
        # Выводим пары

        user_task = Tasks(text=text_task)
        db.session.add(user_task)
        db.session.commit()
        user1.task_id = user_task.id
        user2.task_id = user_task.id

        db.session.add(user1)
        db.session.add(user2)

        db.session.commit()

    return jsonify({}), 200
