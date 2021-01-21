from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[
            DataRequired(),
            Length(1, 64),
            Email()
        ]
    )
    passowrd = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    remember_me = BooleanField('Keep me Logged in')
    submit = SubmitField('Login')