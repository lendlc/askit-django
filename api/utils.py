import random
import string
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

#mail related imports
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

def create_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token


def required_field_err(field):
    return Response(
        {"%s" % field : "%s is required" % field}, 
        status=status.HTTP_400_BAD_REQUEST
    )


def gen_six_digit_code():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))


def send_basic_email(title, body, email_to):
    send_mail(
        title,
        body,
        "Ask IT",
        [email_to],
        fail_silently=False
    )
    return True


def send_html_email(subject, template, data, email_to):
    subject = subject
    context = data
    html_content = render_to_string(template, context)

    msg = EmailMultiAlternatives(
        subject, 
        html_content,
        settings.EMAIL_FROM_NAME,
        to=[email_to],
    )
    
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return True
