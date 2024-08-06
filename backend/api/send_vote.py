from flask import Blueprint, request, jsonify
from .models import db, Users, Tasks, Votes

send_vote_bp = Blueprint('send_vote', __name__)


@send_vote_bp.route('/api/send_vote', methods=['POST'])
def send_vote():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request: No JSON data provided'}), 404

    user_id = data.get('user_id')
    task_id = data.get('task_id')
    vote_value = data.get('vote_value')

    if not user_id or not task_id or vote_value is None:
        return jsonify({'error': 'Missing user_id, task_id, or vote_value'}), 404

    vote_record = Votes(user_id=user_id, task_id=task_id, vote_value=vote_value)
    db.session.add(vote_record)

    try:
        db.session.commit()
        return jsonify({'message': 'Vote processed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
