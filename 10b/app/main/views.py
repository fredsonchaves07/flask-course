from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from . import main
from .forms import EditProfileAdminForm, EditProfileForm, NameForm
from .. import db
from ..models import Permision, User, Role


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

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has ben updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    Role.query.get(form.role.data) = user.role
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
