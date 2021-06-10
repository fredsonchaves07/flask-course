from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import login_required
from ..decorators import admin_required, permission_required
from . import main
from .forms import EditProfileForm, NameForm
from .. import db
from ..models import Permision, User 


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return 'For administrators'

@main.route('/moderate')
@login_required
@permission_required(Permision.MODERATE)
def for_moderators_only():
    return 'For comment moderators'

@main.route('/', methods=['GET', 'POST'])
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


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated')
        
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    
    return render_template('edit_profile.html', form=form)