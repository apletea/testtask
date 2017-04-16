from flask import render_template, url_for, request, flash, redirect, jsonify, abort, g
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import SignupForm, LoginForm, ConnectorForm, flash_errors
from urllib.parse import urlparse, urljoin
from app import app, db, login_manager, api
from app.models import User
import requests

@login_manager.unauthorized_handler
def unauthorized_callback():
  flash('You must be logged in first.', 'info')
  return redirect('/login')

@login_manager.user_loader
def load_user(email):
  return User.query.filter_by(email=email).first()

def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ('http', 'https') and \
    ref_url.netloc == test_url.netloc

@app.route('/')
def home():
  return render_template('home/home.html')

@app.route('/terms-of-service')
def terms_of_service():
  return render_template('home/terms_of_service.html')

@app.route('/privacy-policy')
def privacy_policy():
  return render_template('home/privacy_policy.html')

# A user account page is on the to-do list.
# @app.route('/account', methods=['GET'])
# def account():
#   return render_template('user/account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if request.method == 'POST' and form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()

    if user and user.verify_password(form.password.data):
      login_user(user)
      flash('Welcome back, %s.' % user.name, category='success')

      next = request.args.get('next')

      if not is_safe_url(next):
        return abort(400)

      return redirect(next or url_for('models'))
    else:
      flash("The username or password you have entered is invalid.", category="danger")
  else:
    flash_errors(form)
  return render_template('/user/login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  if request.method == 'POST' and form.validate_on_submit():
    user = User(form.name.data, form.email.data)
    user.hash_password(form.password.data)

    if not User.query.filter_by(email=user.email).count():
      db.session.add(user)
      db.session.commit()
      login_user(user)
      flash("You've successfully signed up!", category="success")

      next = request.args.get('next')

      if not is_safe_url(next):
        return abort(400)

      return redirect(next or url_for('models'))
    else:
      flash("That email is already taken by another user.", category="danger")
  else:
    flash_errors(form)
  return render_template('/user/signup.html', form=form)

@app.route("/logout")
@login_required
def logout():
  logout_user()
  flash("You've been logged out.", category="info")
  return redirect(url_for('models'))

@app.route('/generator/dashboard', methods=['GET'])
def dashboard():
  return render_template('generator/dashboard.html')

# Custom data types is on the to-do list.
# @app.route('/generator/data-types', methods=['GET', 'POST'])
# def data_types():
#   return render_template('generator/data-types.html')

@app.route('/generator/models', methods=['GET'])
@login_required
def models():
  return render_template('generator/models.html')



@app.route('/docs')
def docs():
  return render_template('docs/docs.html')
