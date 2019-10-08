from flask import Blueprint, request, render_template
from werkzeug.security import generate_password_hash

from application import db
from users.models import User
from users.forms import RegisterForm, LoginForm


user_app = Blueprint('user_app', __name__)


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
    return render_template('/register.html', form=form)


@user_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        return 'Logged in'

    return render_template('/login.html', form=form, error=error)