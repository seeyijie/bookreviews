from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, ValidationError
from wtforms.fields.html5 import EmailField
from werkzeug.security import check_password_hash

from users.models import User


class LoginForm(FlaskForm):
    email = EmailField('Email', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.InputRequired(), validators.Length(min=6, max=30)
    ])

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            email=self.email.data
        ).first()

        if user:
            if not check_password_hash(user.password, self.password.data):
                self.password.errors.append('Incorrect email or password')
                return False
            return True
        else:
            self.password.errors.append('Incorrect email or password')
            return False


class RegisterForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    email = EmailField('Email', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.InputRequired(), validators.Length(min=6, max=30)
    ])
    confirm_password = PasswordField('Repeat Password', [
        validators.EqualTo('password', message='Passwords must match')
    ])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already in use, please use a different one.')
