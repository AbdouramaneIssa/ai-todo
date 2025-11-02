"""Gestion de la base de données SQLite pour l'application To-Do List."""

import sqlite3
from typing import List, Optional
from datetime import datetime
from models import Todo


class TodoDatabase:
    """Classe pour gérer les opérations de base de données SQLite."""

    def __init__(self, db_path: str = "todos.db") -> None:
        """Initialise la connexion à la base de données."""
        self.db_path: str = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Crée et retourne une connexion à la base de données."""
        conn: sqlite3.Connection = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """Initialise la base de données en créant les tables."""
        conn: sqlite3.Connection = self.get_connection()
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def create_todo(
        self,
        title: str,
        description: Optional[str] = None
    ) -> Todo:
        """Crée une nouvelle tâche."""
        conn: sqlite3.Connection = self.get_connection()
        cursor: sqlite3.Cursor = conn.cursor()

        now: datetime = datetime.now()
        cursor.execute(
            "INSERT INTO todos (title, description, created_at, updated_at) "
            "VALUES (?, ?, ?, ?)",
            (title, description, now, now)
        )

        conn.commit()
        todo_id: int = int(cursor.lastrowid)
        conn.close()

        return Todo(
            id=todo_id,
            title=title,
            description=description,
            completed=False,
            created_at=now,
            updated_at=now
        )

    def get_all_todos(self) -> List[Todo]:
        """Récupère toutes les tâches."""
        conn: sqlite3.Connection = self.get_connection()
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
        rows: List[sqlite3.Row] = cursor.fetchall()
        conn.close()

        todos: List[Todo] = []
        for row in rows:
            todo: Todo = Todo(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                completed=bool(row['completed']),
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at'])
            )
            todos.append(todo)

        return todos

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """Récupère une tâche spécifique par son ID."""
        conn: sqlite3.Connection = self.get_connection()
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row: Optional[sqlite3.Row] = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return Todo(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            completed=bool(row['completed']),
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )

    def update_todo(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Optional[Todo]:
        """Met à jour une tâche existante."""
        conn: sqlite3.Connection = self.get_connection()
        cursor: sqlite3.Cursor = conn.cursor()

        now: datetime = datetime.now()
        updates: List[str] = []
        params: List[object] = []

        if title is not None:
            updates.append("title = ?")
            params.append(title)

        if description is not None:
            updates.append("description = ?")
            params.append(description)

        if completed is not None:
            updates.append("completed = ?")
            params.append(int(completed))

        if updates:
            updates.append("updated_at = ?")
            params.append(now)
            params.append(todo_id)

            query: str = f"UPDATE todos SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()

        conn.close()
        return self.get_todo_by_id(todo_id)

    def delete_todo(self, todo_id: int) -> bool:
        """Supprime une tâche."""
        conn: sqlite3.Connection = self.get_connection()
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()

        deleted: bool = cursor.rowcount > 0
        conn.close()

        return deleted
