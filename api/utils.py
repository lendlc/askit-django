import random
import string
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

def create_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token


def required_field_err(field):
    return Response(
        {"%s" % field : "%s is required" % field}, 
        status=status.HTTP_400_BAD_REQUEST
    )
    
def send_basic_email(title, body, email_to):
    send_mail(
        title,
        body,
        "Ask IT",
        [email_to],
        fail_silently=False
    )
    return True

def gen_six_digit_code():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
