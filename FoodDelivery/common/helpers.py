from .serializers import CustomerAuthTokenSerializer


from exceptions.generic import CustomBadRequest

from common.constants import PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20, \
    PASSWORD_MUST_HAVE_ONE_NUMBER, PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER, PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER, \
    PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER
from django.core import mail
import re

def save_auth_tokens(authentication_tokens):
    auth_token_serializer = CustomerAuthTokenSerializer(data=authentication_tokens)
    if auth_token_serializer.is_valid():
        auth_token_serializer.save()

def validate_password(password):
    specialCharacters = r"[\$#@!\*]"
    if len(password) < 6:
        return CustomBadRequest(message=PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20)
    if len(password) > 20:
        return CustomBadRequest(message=PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20)
    elif re.search('[0-9]', password) is None:
        return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_NUMBER)
    elif re.search('[a-z]', password) is None:
        return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER)
    elif re.search('[A-Z]', password) is None:
        return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER)
    elif re.search(specialCharacters, password) is None:
        return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER)
    else:
        return True

def send_mail(email, msg):
    with mail.get_connection() as connection:
        mail.EmailMessage(
            "OTP verification for password change",
            msg,
            "dhruvilphotos06@gmail.com",
            email,
            connection=connection,
        ).send()