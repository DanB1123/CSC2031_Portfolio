from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import re

def password_policy_check(form, field):
    password = field.data
    username = form.username.data
    email = form.email.data

    if len(password) < 12:
        raise ValidationError("Password must be at least 12 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must include at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must include at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise ValidationError("Password must include at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must include at least one special character.")
    if re.search(r"\s", password):
        raise ValidationError("Password cannot contain spaces or tabs.")
    if username and username.lower() in password.lower():
        raise ValidationError("Password cannot contain your username.")
    if email and email.split('@')[0].lower() in password.lower():
        raise ValidationError("Password cannot contain your email name part.")

    common_passwords = [
        'password123', 'admin', '123456', 'qwerty', 'letmein',
        'welcome', 'iloveyou', 'abc123', 'monkey', 'football'
    ]
    if password.lower() in common_passwords:
        raise ValidationError("Password is too common. Please choose another one.")

RESERVED_USERNAMES = {'admin', 'root', 'superuser'}
ALLOWED_EMAIL_SUFFIXES = ('.edu', '.ac.uk', '.org')

def ensure_not_reserved(form, field):
    username = (field.data or '').strip()
    if username.lower() in RESERVED_USERNAMES:
        raise ValidationError('This username is unavailable. Please select another.')

def check_username_chars(form, field):
    username = (field.data or '').strip()
    if not re.fullmatch(r'[A-Za-z_]+', username):
        raise ValidationError('Username may contain only letters and underscores (no digits or spaces).')

def check_username_length(form, field):
    username = (field.data or '')
    if not (3 <= len(username) <= 30):
        raise ValidationError('Username must be between 3 and 30 characters.')

def check_email_domain(form, field):
    email = (field.data or '').lower().strip()
    if not any(email.endswith(suffix) for suffix in ALLOWED_EMAIL_SUFFIXES):
        allowed = ', '.join(ALLOWED_EMAIL_SUFFIXES)
        raise ValidationError(f'Email must end with one of: {allowed}')

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            check_username_length,
            check_username_chars,
            ensure_not_reserved
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Invalid email address.'),
            check_email_domain
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            password_policy_check
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    bio = TextAreaField(
        'Bio / Comment',
        validators=[
            Length(max=1000, message='Bio must be 1000 characters or fewer.')
        ]
    )

    submit = SubmitField('Register')
