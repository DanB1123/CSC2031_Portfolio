from flask import Blueprint, render_template, request
from app.forms import RegistrationForm
import bleach
import logging
from datetime import datetime

main = Blueprint('main', __name__)


logging.basicConfig(
    filename='registration.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong', 'a', 'p', 'ul', 'ol', 'li']
ALLOWED_ATTRS = {'a': ['href', 'title']}


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
            attributes=ALLOWED_ATTRS,
            strip=True
        )

        client_ip = request.remote_addr
        logging.info(f"Registration successful: {form.username.data} from {client_ip}")

        return render_template(
            'register.html',
            form=form,
            name=form.username.data,
            bio=sanitized_bio
        )

    if request.method == 'POST':
        client_ip = request.remote_addr
        errors = [f"{field}: {error}" for field, error_list in form.errors.items() for error in error_list]
        logging.warning(f"Validation failed from {client_ip}: {errors}")

    return render_template('register.html', form=form)
