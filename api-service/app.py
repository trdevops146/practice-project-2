from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DB_NAME = os.environ.get('POSTGRES_DB', 'todo')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'postgres')
DB_PORT = os.environ.get('POSTGRES_PORT', '5432')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.order_by(Todo.id).all()
    return jsonify([t.to_dict() for t in todos])

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json(force=True, silent=True) or {}
    title = data.get('title')
    if not title or not isinstance(title, str) or not title.strip():
        abort(400, description="title is required and must be a non-empty string")
    todo = Todo(title=title.strip())
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json(force=True, silent=True) or {}
    if 'title' in data:
        title = data.get('title')
        if not isinstance(title, str) or not title.strip():
            abort(400, description="title must be a non-empty string")
        todo.title = title.strip()
    if 'done' in data:
        todo.done = bool(data.get('done'))
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    # For dev convenience: create tables if missing.
    # In production you should use proper migrations (Alembic / Flask-Migrate).
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
