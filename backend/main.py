from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT
            )
        ''')
        conn.commit()

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

    conn = get_db()
    cursor = conn.cursor()

    # Проверка существования пользователя
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({'message': 'User already registered'}), 200

    try:
        cursor.execute('''
            INSERT INTO users (user_id, username) VALUES (?, ?)
        ''', (user_id, username))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Something went wrong'}), 200

    return jsonify({'message': f'Привет, {username}! Готов к новым приключениям?'}), 200

if __name__ == '__main__':
    init_db()  # Инициализируем базу данных при запуске приложения
    app.run(debug=True)
