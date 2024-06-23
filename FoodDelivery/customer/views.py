import re
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
import random
from rest_framework import status
from django.utils import timezone


from .helpers import validate_password
from common.helpers import save_auth_tokens
from common.models import CustomerAuthTokens
from .serializers import RegistrationSerializer, ResetPasswordSerializer, OTPVerificationSerializer
from .models import Customers, CustomerOTP

from exceptions.generic import CustomBadRequest, BadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse
from common.constants import (PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20, PASSWORD_MUST_HAVE_ONE_NUMBER,
                              PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER, PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER,
                              PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER, EMAIL_ALREADY_EXISTS,
                              USER_REGISTERED_SUCCESSFULLY, BAD_REQUEST,
                              USER_LOGGED_OUT_SUCCESSFULLY, YOUR_PASSWORD_UPDATED_SUCCESSFULLY, OTP_DOESNT_MATCH,
                              OTP_SENT_SUCCESSFULLY, MOBILE_NO_ALREADY_EXISTS,
                              INCORRECT_PASSWORD, WRONG_EMAIL, NEW_PASSWORD_DOESNT_MATCH, OTP_EXPIRED)
from security.customer_authorization import get_authentication_tokens, CustomerJWTAuthentication
from .helpers import send_mail


class Registration(APIView):
    @staticmethod
    def post(request):
        try:
            registration_serializer = RegistrationSerializer(data=request.data)

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

            if "email" in request.data and Customers.objects.filter(email=request.data["email"],
                                                                    is_deleted=False).exists():
                return CustomBadRequest(message=EMAIL_ALREADY_EXISTS)

            if "mobile_no" in request.data and Customers.objects.filter(mobile_no=request.data["mobile_no"],
                                                                    is_deleted=False).exists():
                return CustomBadRequest(message=MOBILE_NO_ALREADY_EXISTS)

            if registration_serializer.is_valid(raise_exception=True):
                customer = registration_serializer.save()
                authentication_tokens = get_authentication_tokens(customer)
                save_auth_tokens(authentication_tokens)
                return GenericSuccessResponse(authentication_tokens, message=USER_REGISTERED_SUCCESSFULLY)
            else:
                return CustomBadRequest(message=BAD_REQUEST)
        except BadRequest as e:
            raise BadRequest(e.detail)
        except Exception as e:
            return GenericException()


class Logout(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def post(request):
        try:
            token = request.headers.get("authorization").split(" ")[1]
            CustomerAuthTokens.objects.filter(access_token=token).delete()
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
            customer = Customers.objects.get(email=email, is_deleted=False)
            if not (password == customer.password):
                raise ValidationError(detail="Incorrect password.")
            authentication_tokens = get_authentication_tokens(customer)
            save_auth_tokens(authentication_tokens)
            return Response(data=authentication_tokens, status=200)
        except Customers.DoesNotExist:
            raise NotFound(detail="Email not found.")
        except Exception as e:
            return Response(data={"message": "An unexpected error occurred."}, status=500)


class ResetPassword(APIView):
    @staticmethod
    def patch(request):
        try:
            if "email" not in request.data or "new_password" not in request.data or "confirm_password" not in request.data:
                raise CustomBadRequest(message=BAD_REQUEST)
            new_password = request.data["new_password"]
            confirm_password = request.data["confirm_password"]
            email = request.data["email"]
            customer = Customers.objects.get(email=email, is_deleted=False)
            if not (check_password == customer.password):
                if new_password == confirm_password:
                    if validate_password(confirm_password):
                        customer.password = make_password(new_password)
                        customer.save()
                        return GenericSuccessResponse('e', message=YOUR_PASSWORD_UPDATED_SUCCESSFULLY)
                else:
                    return CustomBadRequest(message=NEW_PASSWORD_DOESNT_MATCH)
            else:
                return CustomBadRequest(message=INCORRECT_PASSWORD)
        except Exception as e:
            return GenericException()


class OTPVerification(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            if not email:
                return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
            otp = str(random.randint(1000, 9999))
            try:
                customer = Customers.objects.get(email=email, is_deleted=False)
            except Customers.DoesNotExist:
                return Response({"error": WRONG_EMAIL}, status=status.HTTP_400_BAD_REQUEST)
            otp_verification_data = {
                "otp": otp,
                "customer_id": customer.id
            }
            otpverification_serializer = OTPVerificationSerializer(data=otp_verification_data)
            if otpverification_serializer.is_valid():
                otpverification_serializer.save()
                send_mail([email], msg=otp)
                return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(otpverification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForgotPassword(APIView):
    @staticmethod
    def patch(request):
        try:
            if "email" not in request.data or "new_password" not in request.data or "confirm_password" not in request.data or "otp" not in request.data:
                raise CustomBadRequest(message=BAD_REQUEST)
            new_password = request.data["new_password"]
            confirm_password = request.data["confirm_password"]
            email = request.data["email"]
            otp = request.data["otp"]
            del request.data["new_password"]
            del request.data["confirm_password"]
            del request.data["email"]
            del request.data["otp"]
            resetpassword_serializer = ResetPasswordSerializer(data=request.data)
            customer = Customers.objects.get(email=email, is_deleted=False)
            customer_otp = CustomerOTP.objects.filter(customer_id=customer.id).last()
            print("customer otp", customer_otp.created_at)
            if new_password == confirm_password:
                if (timezone.now() - customer_otp.created_at < timezone.timedelta(minutes=2)):
                    if customer_otp.otp == otp:
                        if validate_password(confirm_password):
                            request.data["password"] = make_password(new_password)
                            if resetpassword_serializer.is_valid():
                                resetpassword_serializer.update(customer, resetpassword_serializer.validated_data)
                                return GenericSuccessResponse('e', message=YOUR_PASSWORD_UPDATED_SUCCESSFULLY)
                    else:
                        return CustomBadRequest(message=OTP_DOESNT_MATCH)
                else:
                    return CustomBadRequest(message=OTP_EXPIRED)
            else:
                return CustomBadRequest(message=NEW_PASSWORD_DOESNT_MATCH)
        except Exception as e:
            return GenericException()


