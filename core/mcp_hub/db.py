import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "intellify_tasks.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                service_id TEXT,
                status TEXT,
                progress TEXT,
                started_at TEXT,
                npu_status TEXT
            )
        """)
        conn.commit()

def create_task(task_id: str, service_id: str, status: str, progress: str, started_at: str):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (task_id, service_id, status, progress, started_at) VALUES (?, ?, ?, ?, ?)",
            (task_id, service_id, status, progress, started_at)
        )
        conn.commit()

def update_task_status(task_id: str, status: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE task_id = ?", (status, task_id))
        conn.commit()

def update_task_npu_status(task_id: str, npu_status: dict):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET npu_status = ? WHERE task_id = ?", (json.dumps(npu_status), task_id))
        conn.commit()

def get_task(task_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
        row = cursor.fetchone()
        if row:
            d = dict(row)
            if d['npu_status']:
                d['npu_status'] = json.loads(d['npu_status'])
            return d
        return None

def get_all_tasks():
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        
        result = {}
        for row in rows:
            d = dict(row)
            if d['npu_status']:
                d['npu_status'] = json.loads(d['npu_status'])
            result[d['task_id']] = d
        return result
