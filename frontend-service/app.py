from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')  # change in production

# Default API URL; you will set this via env in containers/k8s
API_URL = os.environ.get('API_URL', 'http://localhost:5001')

@app.route('/')
def index():
    todos = []
    try:
        resp = requests.get(f"{API_URL}/todos", timeout=2)
        if resp.ok:
            todos = resp.json()
    except Exception:
        flash("Could not reach backend API. Check API_URL and network.", "error")
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if not title:
        flash("Title cannot be empty", "error")
        return redirect(url_for('index'))

    try:
        resp = requests.post(f"{API_URL}/todos", json={"title": title}, timeout=2)
        if not resp.ok:
            flash(f"API error: {resp.status_code}", "error")
    except Exception:
        flash("Failed to call API to create todo.", "error")

    return redirect(url_for('index'))
