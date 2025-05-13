from flask import render_template, redirect, url_for, flash, request, session, g, current_app
from urllib.parse import urlparse
from app import db
from app.auth import auth_bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from functools import wraps
from datetime import datetime



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', 'success')
            session.clear()
            session['user_id'] = user.id
            session.permanent = True
            session['last_activity'] = datetime.utcnow().isoformat()
            g.user = user
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {e}', 'danger')
    return render_template('register.html', title='Register', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

        session.clear()
        session['user_id'] = user.id
        g.user = user

        if form.remember_me.data:
            session.permanent = True
        else:
            session.permanent = False

        session['last_activity'] = datetime.utcnow().isoformat()

        flash(f'Welcome back, {user.username}!', 'success')
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    g.user = None
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))