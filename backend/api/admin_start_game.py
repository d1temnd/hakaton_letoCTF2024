from flask import Blueprint, request, jsonify
from .models import db, Users, Tasks
import random
import json

admin_start_game_bp = Blueprint('admin_start_game', __name__)


@admin_start_game_bp.route("/api/admin/start_game", methods=['POST'])
def admin_start_game():
    # Найти пользователя с данным user_id
    users = Users.query.all()
    if not users:
        return jsonify({'error': 'User not found'}), 404

    random.shuffle(users)

    # Создаем пары
    pairs = []
    for i in range(0, len(users), 2):
        pair = users[i:i + 2]
        if len(pair) == 2:
            pairs.append(pair)
    print(pairs)
    for pair in pairs:
        user1 = pair[0]
        user2 = pair[1]

        with open('words/task.json', encoding="utf-8") as f:
            data = json.load(f)

        obj = random.choice(data["object"])
        selected_prop = random.choice(list(obj["prop"].keys()))

        action = random.choice(data["action"])
        place = random.choice(data["place"])
        prop = random.choice(obj["prop"][selected_prop])
        obj = random.choice(obj["obj"])

        text_task = f'{user1.username}, {user2.username}:\nДействие: {action}.\nОбъект: {prop} {obj}.\nМесто: {place}.'
        # Выводим пары

        usertask = Tasks(text=text_task)
        db.session.add(usertask)
        db.session.commit()
        user1.task_id = usertask.id
        user2.task_id = usertask.id

        db.session.add(user1)
        db.session.add(user2)

        db.session.commit()

        print(usertask.id)

    return jsonify({}), 200
