from dotenv import load_dotenv
import os

import psycopg

from flask import Flask, render_template, request, redirect, flash, get_flashed_messages, url_for

from repository import UserRepository
from validator import validate


load_dotenv()

database_url = os.getenv("DATABASE_URL")
conn = psycopg.connect(database_url)
conn.autocommit = True
repo = UserRepository(conn)

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route('/')
def index():
    return render_template(
        'users/main_page.html'
    )


@app.get('/users/')
def get_users():
    messages = get_flashed_messages(with_categories=True)
    query = request.args.get('query', '')
    if query:
        users = repo.get_by_term(query)
    else:
        users = repo.get_content()
    return render_template(
        'users/users.html',
        search=query,
        users=users,
        messages=messages,
        hide_sidebar=True
    )


@app.post('/users/')
def users_post():
    user_data = request.form.to_dict()
    errors = validate(user_data)
    if errors:
        return render_template(
            'users/new_user.html',
            user=user_data,
            errors=errors
        ), 422
    repo._create(user_data)
    flash(f"Пользователь {user_data['username']} успешно зарегистрирован", "success")
    return redirect(url_for('get_users'), code=302)


@app.route('/users/<id>')
def show_user(id):
    user = repo.find(id)
    if user is None:
        return 'Page not found', 404
    return render_template(
        'users/show_user.html',
        user=user
    )

@app.route('/users/new')
def users_new():
    """Обработчик "users_new()" является формой для регистрации пользователя"""
    return render_template(
        'users/new_user.html',
        user={},
        errors={}
    )


@app.route('/users/<id>/update', methods=['GET', 'POST'])
def users_update(id):
    user = repo.find(id)
    if request.method == 'GET':
        return render_template(
            'users/edit_user.html',
            user=user,
            errors={},
        )
    if request.method == 'POST':
        users_data = request.form.to_dict()
        errors = validate(users_data)
        if errors:
            return render_template(
                'users/edit_user.html',
                user=users_data,
                errors=errors
            ), 422
        user = {'id': id, 'username': users_data['username'], 'email': users_data['email']}
        repo.save(user)
        flash(f'User {user['username']} has been updated', 'success')
        return redirect(url_for('get_users'), code=302)


@app.post('/users/<id>/delete')
def users_delete(id):
    user = repo.find(id)
    repo.destroy(user)
    flash(f'User {user['username']} has been deleted', 'success')
    return redirect(url_for('get_users'), code=302)
