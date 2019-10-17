from flask import Blueprint, render_template, redirect, session, url_for, request
from werkzeug.security import generate_password_hash

from application import db
from users.models import User
from users.forms import RegisterForm, LoginForm
from models.logs import LoggerObject

user_app = Blueprint('user_app', __name__)

logger = LoggerObject()

@user_app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # import pdb; pdb.set_trace() # for troubleshooting
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            form.name.data,
            form.email.data,
            hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return f'User ID: {user.id}'    
    logger.logrequest(request)
    return render_template('register.html', form=form)

@user_app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('name'):
        return "You are already logged in!"

    form = LoginForm()
    error = None

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        session['id'] = user.id
        session['name'] = user.name
        # Redirection
        # '.register' if same file. Otherwise have to specify app.function
        logger.logrequest(request)
        return redirect(url_for('.register'))

    logger.logrequest(request)
    return render_template('login.html', form=form, error=error)


@user_app.route('/logout')
def logout():
    session.pop('id')
    session.pop('name')
    logger.logrequest(request)
    return redirect(url_for('.login'))