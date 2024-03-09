from flask import redirect, render_template, url_for
from flask_login import login_required
from app import app
from app.models.db.db_model import Task
from app.models.forms.task_form import TaskForm
from app.services.session_scope import session_scope

@app.route('/tasks', methods=['GET'])
def get_tasks():
    with session_scope() as session:
        tasks = session.query(Task).all()
    return render_template('task/tasks.html', tasks=tasks)

@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(description=form.description.data, user_id=form.user_id.data)
        with session_scope() as session:
            session.add(new_task)
        return redirect(url_for('get_tasks'))
    return render_template('task/create_task.html', form=form)

@app.route('/tasks/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    form = TaskForm()
    if form.validate_on_submit():
        with session_scope() as session:
            task = session.query(Task).filter_by(id=id).first()
            task.description = form.description.data
        return redirect(url_for('get_tasks'))
    return render_template('task/update_task.html', form=form)

@app.route('/tasks/delete/<int:id>', methods=['POST'])
def delete_task(id):
    with session_scope() as session:
        task = session.query(Task).filter_by(id=id).first()
        session.delete(task)
    return redirect(url_for('get_tasks'))