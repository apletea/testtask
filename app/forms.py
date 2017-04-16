from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import Length, Email, InputRequired, EqualTo, URL, NumberRange

def flash_errors(form):
  for field, errors in form.errors.items():
    for error in errors:
      flash("Error in the %s field - %s" % (getattr(form, field).label.text, error), category="danger")

class LoginForm(FlaskForm):
  email = StringField('email', [InputRequired(), Email()])
  password = PasswordField('password', [InputRequired()])

class SignupForm(FlaskForm):
  email = StringField('email', [Email()])
  password = PasswordField('password', [Length(min=6, max=35)])
  confirmation = PasswordField('confirmation', [InputRequired(), EqualTo('password', message='Passwords must match.')])

class ConnectorForm(FlaskForm):
  username = StringField('username', [InputRequired()])
  password = PasswordField('password', [InputRequired()])
  endpoint = StringField('endpoint', [InputRequired(), URL(require_tld=False)])
  model = SelectField('model', [InputRequired()])
  amount = IntegerField('amount', [InputRequired(), NumberRange(min=1, max=100)])