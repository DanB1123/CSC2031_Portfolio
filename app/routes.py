from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import RegistrationForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.register'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()


    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        flash(f'Registration successful for {username}!', 'success')
        return render_template('register.html', form=form, name=username)
    return render_template('register.html', form=form)
