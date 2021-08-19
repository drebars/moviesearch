from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.datetime_safe import datetime
from django.utils.html import strip_tags
import jwt


def send_activation_code(email, activation_code, status):
    if status == 'register':
        url =f'http://localhost:7000/api/v1/activate/{activation_code}'
        message = f'Code: {url}'
        send_mail('Activate your account !', message, 'stackoverflow_adminLOL@gmail.com', [email],
                                    fail_silently=False)
    elif status == 'reset_password':
        send_mail('Reset your Password', f"Код Активации:{activation_code}", 'StackOverFlow_admin@gmail.com', [email, ],
                  fail_silently=False)

#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