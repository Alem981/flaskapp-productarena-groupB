from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from productarena.models import Doctor


class RegisterForm(FlaskForm):
  def validate_email_address(self, email_address_to_check):
    email_address = Doctor.query.filter_by(email_address=email_address_to_check.data).first()
    if email_address:
      raise ValidationError('Email address already exists! Please try a different email address')
  first_name = StringField(label='First Name:', validators=[DataRequired()])
  last_name = StringField(label='Last Name:', validators=[DataRequired()])
  email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
  password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
  password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
  submit = SubmitField(label='Add Doctor')


class LoginForm(FlaskForm):
  email_address = StringField(label='Email:', validators=[DataRequired()])  
  password = PasswordField(label='Password:',  validators=[DataRequired()])
  submit = SubmitField(label='Log In')
