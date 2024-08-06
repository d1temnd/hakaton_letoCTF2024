from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    telegram_id = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer, default=0)
    task_id = db.Column(db.Integer, nullable=False)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    path_to_file = db.Column(db.String(255), nullable=True)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)


@app.route('/api/start', methods=['POST'])
def start():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'error': f'Invalid request: {str(e)}'}), 400

    user_id = data.get('user_id')
    username = data.get('username')

    if not user_id or not username:
        return jsonify({'error': 'Missing user_id or username'}), 400

    existing_user = User.query.filter_by(user_id=user_id).first()

    if existing_user:
        return jsonify({'message': 'User already registered'}), 200

    try:
        new_user = User(user_id=user_id, username=username)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({'message': 'Something went wrong: ' + str(e)}), 500

    return jsonify({'message': f'Привет, {username}! Готов к новым приключениям?'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Инициализируем базу данных при запуске приложения
    app.run(debug=True)
