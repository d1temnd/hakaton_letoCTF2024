from flask import Blueprint, request, jsonify
from .models import db, Users, Tasks, Votes
from sqlalchemy import func

admin_end_game_bp = Blueprint('admin_end_game', __name__)


@admin_end_game_bp.route('/api/admin/end_game', methods=['POST', 'GET'])
def end_game():
    try:
        # Calculate votes for each user
        user_votes = db.session.query(
            Votes.user_id,
            func.count(Votes.id).label('vote_count')
        ).group_by(Votes.user_id).all()

        print("User Votes:", user_votes)  # Debugging line

        for user_id, vote_count in user_votes:
            user = Users.query.filter_by(user_id=user_id).first()
            if user:
                user.score += vote_count * 5
            else:
                print(f"User with ID {user_id} not found.")  # Debugging line

        # Calculate average vote for each task
        task_avg_votes = db.session.query(
            Votes.task_id,
            func.avg(Votes.vote_value).label('avg_vote'),
            func.sum(Votes.id).label('count_vote')
        ).group_by(Votes.task_id).all()

        print("Task Avg Votes:", task_avg_votes)  # Debugging line

        for task_id, avg_vote, count_vote in task_avg_votes:
            task_score = int(avg_vote * count_vote * 5)
            users_with_task = Users.query.filter_by(task_id=task_id).all()
            for user in users_with_task:
                user.score += task_score

                print(user.score)

        # Commit changes to the database
        db.session.commit()

        # удалить все
        db.session.query(Tasks).delete()
        db.session.query(Votes).delete()
        db.session.commit()

        return jsonify({"message": "Game ended and scores updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")  # Debugging line
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

