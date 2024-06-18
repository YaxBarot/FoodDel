import re
from rest_framework.views import APIView

from .serializers import RegistrationSerializer
from .models import Customers

from exceptions.generic import CustomBadRequest, BadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse
from common.constants import PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20, PASSWORD_MUST_HAVE_ONE_NUMBER, \
    PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER, PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER, \
    PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER, EMAIL_ALREADY_EXISTS, USER_REGISTERED_SUCCESSFULLY, BAD_REQUEST
from security.customer_authorization import get_authentication_tokens, CustomerJWTAuthentication
from common.helpers import save_auth_tokens


class Registration(APIView):
    @staticmethod
    def post(request):
        try:
            registration_serializer = RegistrationSerializer(data=request.data)

            if "password" in request.data:

                password = request.data["password"]

                specialCharacters = r"[\$#@!\*]"

                if len(password) < 6:
                    return CustomBadRequest(message=PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20)
                elif len(password) > 20:
                    return CustomBadRequest(message=PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20)
                elif re.search('[0-9]', password) is None:
                    return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_NUMBER)
                elif re.search('[a-z]', password) is None:
                    return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER)
                elif re.search('[A-Z]', password) is None:
                    return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER)
                elif re.search(specialCharacters, password) is None:
                    return CustomBadRequest(message=PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER)

            print("hii")
            if "email" in request.data and Customers.objects.filter(email=request.data["email"],
                                                                    is_deleted=False).exists():
                return CustomBadRequest(message=EMAIL_ALREADY_EXISTS)

            if registration_serializer.is_valid(raise_exception=True):
                print("inside_if")
                customer = registration_serializer.save()

                authentication_tokens = get_authentication_tokens(customer)
                save_auth_tokens(authentication_tokens)

                return GenericSuccessResponse(authentication_tokens, message=USER_REGISTERED_SUCCESSFULLY)

            else:
                print("hello")
                return CustomBadRequest(message=BAD_REQUEST)

        except BadRequest as e:
            raise BadRequest(e.detail)

        except Exception as e:
            print(e)
            return GenericException()


class Test(APIView):
    authentication_classes = [CustomerJWTAuthentication]
    @staticmethod
    def post(request):
        print(request.user)
        return GenericSuccessResponse("authentication_tokens", message=USER_REGISTERED_SUCCESSFULLY)
