import re
import traceback
from django.shortcuts import render
from rest_framework.response import Response


from common.models import AdministratorAuthTokens, CustomerAuthTokens
from security.administration_authorization import AdministratorJWTAuthentication, save_administrator_auth_tokens
from common.helpers import save_auth_tokens
from security.administration_authorization import get_authentication_tokens
from administrator.models import Administrator
from administrator.serializer import AdminRegistrationSerializer
from common.constants import BAD_REQUEST, EMAIL_ALREADY_EXISTS, PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20, PASSWORD_MUST_HAVE_ONE_NUMBER, PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER, PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER, PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER, USER_LOGGED_OUT_SUCCESSFULLY, USER_REGISTERED_SUCCESSFULLY
from customer.serializers import RegistrationSerializer
from exceptions.generic import BadRequest, CustomBadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
# Create your views here.

class Registration(APIView):
    @staticmethod
    def post(request):
        try:
            admin_registration_serializer = AdminRegistrationSerializer(data=request.data)

            if "password" in request.data:
                password = request.data["password"]
                special_characters = r"[\$#@!\*]"

                if len(password) < 8 or len(password) > 20:
                    return CustomBadRequest(message=PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20)
                elif re.search('[0-9]', password) is None:
                    return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_NUMBER)
                elif re.search('[a-z]', password) is None:
                    return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER)
                elif re.search('[A-Z]', password) is None:
                    return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER)
                elif re.search(special_characters, password) is None:
                    return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER)

            if "email" in request.data and Administrator.objects.filter(email=request.data["email"],
                                                                    is_deleted=False).exists():
                return CustomBadRequest(message=EMAIL_ALREADY_EXISTS)
            
            if admin_registration_serializer.is_valid(raise_exception=True):
                admin = admin_registration_serializer.save()
                authentication_tokens = get_authentication_tokens(admin)
                save_administrator_auth_tokens(authentication_tokens)
                return GenericSuccessResponse(authentication_tokens, message=USER_REGISTERED_SUCCESSFULLY)
            else:
                return CustomBadRequest(message=BAD_REQUEST)
        except BadRequest as e:
            raise BadRequest(e.detail)
        except Exception as e:
            traceback.print_exc()
            return GenericException()


class Logout(APIView):
    authentication_classes = [AdministratorJWTAuthentication]

    @staticmethod
    def post(request):
        try:
            token = request.headers.get("authorization").split(" ")[1]
            AdministratorAuthTokens.objects.filter(access_token=token).delete()
            
            return GenericSuccessResponse(message=USER_LOGGED_OUT_SUCCESSFULLY)
        except Exception as e:
            return GenericException()


class Login(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            if not email or not password:
                raise ValidationError(detail="Email and password are required.")
            administrator = Administrator.objects.get(email=email, is_deleted=False)
            if not (password == administrator.password):
                raise ValidationError(detail="Incorrect password.")
            authentication_tokens = get_authentication_tokens(administrator)
            save_administrator_auth_tokens(authentication_tokens)
            return Response(data=authentication_tokens, status=200)
        except Administrator.DoesNotExist:
            raise NotFound(detail="Email not found.")
        except Exception as e:
            traceback.print_exc()
            return GenericException()
