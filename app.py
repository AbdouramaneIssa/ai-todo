"""Application Flask pour la To-Do List avec API REST typée."""

from flask import Flask, render_template, request, jsonify
from typing import Dict, Any, Tuple, List
from database import TodoDatabase

app: Flask = Flask(__name__)
db: TodoDatabase = TodoDatabase("todos.db")


@app.route("/")
def index() -> str:
    """Page d'accueil avec la To-Do List."""
    return render_template("index.html")


@app.route("/api/todos", methods=["GET"])
def get_todos() -> Tuple[Dict[str, Any], int]:
    """Récupère toutes les tâches."""
    try:
        todos = db.get_all_todos()
        todos_data: List[Dict[str, Any]] = [todo.to_dict() for todo in todos]
        return jsonify({"success": True, "data": todos_data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/todos", methods=["POST"])
def create_todo() -> Tuple[Dict[str, Any], int]:
    """Crée une nouvelle tâche."""
    try:
        data: Dict[str, Any] = request.get_json()
        if not data or "title" not in data:
            msg = "Title is required"
            return jsonify({"success": False, "error": msg}), 400

        todo = db.create_todo(
            title=data["title"],
            description=data.get("description")
        )
        return jsonify({"success": True, "data": todo.to_dict()}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id: int) -> Tuple[Dict[str, Any], int]:
    """Récupère une tâche spécifique."""
    try:
        todo = db.get_todo_by_id(todo_id)
        if todo is None:
            msg = "Todo not found"
            return jsonify({"success": False, "error": msg}), 404
        return jsonify({"success": True, "data": todo.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id: int) -> Tuple[Dict[str, Any], int]:
    """Met à jour une tâche."""
    try:
        data: Dict[str, Any] = request.get_json()
        todo = db.update_todo(
            todo_id,
            title=data.get("title"),
            description=data.get("description"),
            completed=data.get("completed")
        )
        if todo is None:
            msg = "Todo not found"
            return jsonify({"success": False, "error": msg}), 404
        return jsonify({"success": True, "data": todo.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id: int) -> Tuple[Dict[str, Any], int]:
    """Supprime une tâche."""
    try:
        success: bool = db.delete_todo(todo_id)
        if not success:
            msg = "Todo not found"
            return jsonify({"success": False, "error": msg}), 404
        msg_ok = "Todo deleted"
        return jsonify({"success": True, "message": msg_ok}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
