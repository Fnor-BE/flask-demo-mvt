from flask import redirect, render_template, url_for
from flask_login import login_user, logout_user, login_required
from app import app, login_manager
from app.models.db.db_model import User
from app.models.forms.login_form import LoginForm
from app.models.forms.register_form import RegisterForm
from app.services.Security import hash_password, verify_password
from app.services.session_scope import session_scope

@login_manager.user_loader
def load_user(id):
    with session_scope() as session:
        return session.query(User).filter_by(id=id).first()

@app.route('/auth/login', methods=['GET','POST'])
def login():
    newLoginForm = LoginForm()
    
    if newLoginForm.validate_on_submit():
        try:
            with session_scope() as session:
                # Récupérez l'utilisateur à partir du formulaire
                user = session.query(User).filter_by(email=newLoginForm.email.data).first()
                if user and verify_password(user.password, newLoginForm.password.data):
                    login_user(user)
                    # print("Authentification réussie pour l'utilisateur:", user.username)
                    return redirect(url_for('index'))
                
                else:
                    # print("Échec de l'authentification pour l'utilisateur:", newLoginForm.email.data) 
                    return render_template('auth/login.html', newLoginForm=newLoginForm)
        except Exception as e:
            print(f"Une erreur s'est produite lors de la connexion : {e}")
            return redirect(url_for('login'))
    
    return render_template('auth/login.html', newLoginForm=newLoginForm)


@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    newRegisterForm = RegisterForm()

    if newRegisterForm.validate_on_submit():
        new_user = User(
            username=newRegisterForm.username.data,
            email=newRegisterForm.email.data,
            password=hash_password(newRegisterForm.password.data)
        )

        try:
            with session_scope() as session:
                session.add(new_user)
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'ajout de l'utilisateur : {e}")
            return redirect(url_for('index'))

        return redirect(url_for('login'))

    return render_template('auth/register.html', newRegisterForm=newRegisterForm)

@app.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))