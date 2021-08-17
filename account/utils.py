from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.datetime_safe import datetime
from django.utils.html import strip_tags
import jwt


def send_activation_code(email, activation_code):
    context = {
        'text_detail': 'Thank you for registration on our site! LOL!',
        'email': email,
        'domain': 'http://localhost:8000',
        'activation_code': activation_code
    }
    msg_html = render_to_string('email.html', context)
    message = strip_tags(msg_html)
    send_mail('Activate your account LOL!', message, 'stackoverflow_adminLOL@gmail.com', [email], html_message=msg_html,
                                fail_silently=False)

def generate_access_token(user):
    payload = {
                'exp': datetime.utcnow() + timedelta(days=1, minutes=0),
                'iat': datetime.utcnow(),}
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token

#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