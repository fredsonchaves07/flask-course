from flask import Flask, render_template, session, redirect, url_for, flash, current_app
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Desenvolvedor Python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'c0ce86e978a7d3'
app.config['MAIL_PASSWORD'] = '39feb26c850205'
app.config['FLASK_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASK_MAIL_SENDER'] = 'Flask Admin <flasky@example.com>'
app.config['FLASK_ADMIN'] = os.environ.get('FLASK_ADMIN')

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


# Models
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class NameForm(FlaskForm):
    name = StringField('Informe o seu nome: ', validators=[DataRequired()])
    submit = SubmitField('Enviar')


#Mail
def send_email(to, subject, template, **kwargs):
    msg = Message(
        app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subject, 
        sender=app.config['FLASK_MAIL_SENDER'],
        recipients=[to]
    )

    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()

        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASK_ADMIN']:
                send_email(
                    app.config['FLASK_ADMIN'], 
                    'New User',
                    'mail/new_user',
                    user=user
                )
        else:
            session['known'] = True    
            session['name'] = form.name.data
            form.name.data = ''
            return redirect(url_for('index'))

        return render_template(
            'index.html', 
            form=form, 
            name=session.get('name'), 
            known=session.get('known', False)
        )

        
    return render_template('index.html',
                            current_time=datetime.utcnow(),
                            form=form,
                            name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error_serve(e):
    return render_template('500.html'), 500
