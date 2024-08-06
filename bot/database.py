import sqlite3

conn = sqlite3.connect("bot.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()


def get_topics() -> list:
    """
    Получить все топики
    """
    cur.execute("""SELECT * FROM topics""")
    return cur.fetchall()


def get_topic(id: int):
    """
    Получить топик по id
    """
    cur.execute("""SELECT * FROM topics WHERE id = ?""", (id, ))
    return cur.fetchone()


def get_tasks() -> list:
    """
    Получить все задания
    """
    cur.execute("""SELECT * FROM tasks""")
    return cur.fetchall()


def get_task(id: int):
    """
    Получить задание по id
    """
    cur.execute("""SELECT * FROM tasks WHERE id = ?""", (id, ))
    return cur.fetchone()


def get_all() -> list:
    """
    Получение всего для поиска
    """
    cur.execute("""
    SELECT 'topic=' || id AS data, name AS text FROM topics
    UNION
    SELECT 'topic=' || id AS data, desc AS text FROM topics
    UNION
    SELECT 'task=' || id AS data, name AS text FROM tasks
    UNION
    SELECT 'task=' || id AS data, desc AS text FROM tasks
    """)
    return cur.fetchall()


def get_topic_tasks(topic_id: int) -> list:
    """
    Получить соответсвенные задания для темы
    """
    cur.execute("""
    SELECT tasks.id AS id, tasks.name AS name
    FROM topic_tasks
    JOIN tasks ON tasks.id = topic_tasks.task_id
    WHERE topic_tasks.topic_id = ?
    """, (topic_id, ))
    return cur.fetchall()


def get_task_topics(task_id: int) -> list:
    """
    Получить соответсвенные темы для задания
    """
    cur.execute("""
    SELECT topics.id AS id, topics.name AS name
    FROM topic_tasks
    JOIN topics ON topics.id = topic_tasks.topic_id
    WHERE topic_tasks.task_id = ?
    """, (task_id, ))
    return cur.fetchall()