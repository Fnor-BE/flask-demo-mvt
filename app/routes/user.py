from flask import redirect, render_template, url_for
from flask_login import login_required, current_user
from app import app
from app.models.db.db_model import Task
from app.models.forms.task_form import TaskForm
from app.services.session_scope import session_scope

@app.route('/user/profil', methods=['GET'])
@login_required
def profil():
    return render_template('user/profil.html', username=current_user.username)
