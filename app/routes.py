from flask import Blueprint, render_template, request
from app.forms import RegistrationForm
import bleach

main = Blueprint('main', __name__)

ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong', 'a', 'p', 'ul', 'ol', 'li']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}


@main.route('/', methods=['GET'])
def home():
    return render_template('register.html', form=RegistrationForm())


@main.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        raw_bio = form.bio.data or ""

        sanitized_bio = bleach.clean(
            raw_bio,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )

        return render_template(
            'register.html',
            form=form,
            name=form.username.data,
            bio=sanitized_bio
        )

    return render_template('register.html', form=form)