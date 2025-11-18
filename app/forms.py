from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError

RESERVED_USERNAMES = ['admin', 'root', 'superuser']
ALLOWED_DOMAINS = ['.edu', '.ac.uk', '.org']
COMMON_PASSWORDS = [
    'password123', 'admin', '123456', 'qwerty', 'letmein',
    'welcome', 'iloveyou', 'abc123', 'monkey', 'football'
]

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            Regexp(r'^[A-Za-z_]+$', message="Letters and underscores only")
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message="Invalid email")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=12, message="Minimum 12 characters")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match")
        ]
    )
    bio = TextAreaField('Bio / Comment')
    submit = SubmitField('Register')

    def validate_username(self, field):
        if field.data.lower() in RESERVED_USERNAMES:
            raise ValidationError("This username is reserved.")

    def validate_email(self, field):
        if not any(field.data.endswith(domain) for domain in ALLOWED_DOMAINS):
            raise ValidationError("Email domain not allowed.")

    def validate_password(self, field):
        pw = field.data
        uname = self.username.data.lower()
        email = self.email.data.lower()
        import re

        if uname in pw.lower() or email in pw.lower():
            raise ValidationError("Password must not contain username or email")
        if any(pw.lower() == p.lower() for p in COMMON_PASSWORDS):
            raise ValidationError("Password is too common")
        if re.search(r'\s', pw):
            raise ValidationError("Password must not contain whitespace")
        if not re.search(r'[A-Z]', pw):
            raise ValidationError("Password must contain an uppercase letter")
        if not re.search(r'[a-z]', pw):
            raise ValidationError("Password must contain a lowercase letter")
        if not re.search(r'\d', pw):
            raise ValidationError("Password must contain a digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', pw):
            raise ValidationError("Password must contain a special character")