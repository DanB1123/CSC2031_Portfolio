import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

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

    # Part B will replace
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, message='Password must be at least 8 characters (placeholder for Part B).')
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
