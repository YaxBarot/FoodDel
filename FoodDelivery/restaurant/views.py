from django.shortcuts import render
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password

import datetime
import smtplib
import traceback
import pytz
import re
import random

from security.restaurant_authorization import get_restaurant_authentication_tokens, \
    save_restaurant_auth_tokens, RestaurantJWTAuthentication

from exceptions.generic_response import GenericSuccessResponse

from exceptions.generic import CustomBadRequest,GenericException

from common.models import RestaurantAuthTokens

from common.helpers import send_mail, validate_password

from common.constants import EMAIL_ALREADY_EXISTS, USER_REGISTERED_SUCCESSFULLY, BAD_REQUEST, \
    USER_LOGGED_OUT_SUCCESSFULLY, USER_LOGGED_IN_SUCCESSFULLY, INCORRECT_PASSWORD, WRONG_EMAIL, \
    YOUR_PASSWORD_UPDATED_SUCCESSFULLY, NEW_PASSWORD_DOESNT_MATCH, OTP_SENT_SUCCESSFULLY, OTP_DOESNT_MATCH, OTP_EXPIRED, \
        PASSWORD_LENGTH_SHOULD_BE_BETWEEN_8_TO_20, \
    PASSWORD_MUST_HAVE_ONE_NUMBER, PASSWORD_MUST_HAVE_ONE_SMALLERCASE_LETTER, PASSWORD_MUST_HAVE_ONE_UPPERCASE_LETTER, \
    PASSWORD_MUST_HAVE_ONE_SPECIAL_CHARACTER


from .models import RestaurantOTP, RestaurantProfile, RestaurantType

from .serializers import RegistrationSerializer, ResetPasswordSerializer, OTPVerificationSerializer



# Create your views here.


class Registration(APIView):
    @staticmethod
    def post(request):
        try:
            registration_serializer = RegistrationSerializer(data=request.data)

            if "email" in request.data and RestaurantProfile.objects.filter(email=request.data["email"],
                                                                        is_deleted=False).exists():
                return CustomBadRequest(message=EMAIL_ALREADY_EXISTS)

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

                request.data["password"] = make_password(request.data["password"])

            if registration_serializer.is_valid():
                restaurant = registration_serializer.save()

                authentication_tokens = get_restaurant_authentication_tokens(restaurant)
                save_restaurant_auth_tokens(authentication_tokens)

                return GenericSuccessResponse(authentication_tokens, message=USER_REGISTERED_SUCCESSFULLY)
            
            else:
                return CustomBadRequest(message=BAD_REQUEST)

        except Exception as e:
            return GenericException()


class Logout(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    @staticmethod
    def post(request):
        try:
            token = request.headers.get("authorization").split(" ")[1]
            
            RestaurantAuthTokens.objects.filter(access_token=token).delete()

            return GenericSuccessResponse(message=USER_LOGGED_OUT_SUCCESSFULLY)
        
        except Exception as e:
            return GenericException()


class Login(APIView):
    @staticmethod
    def post(request):
        try:
            if "email" not in request.data or "password" not in request.data:
                raise CustomBadRequest(message=BAD_REQUEST)

            restaurant = RestaurantProfile.objects.get(email=request.data["email"],
                                               is_deleted=False)

            if check_password(request.data["password"], restaurant.password):
                authentication_tokens = get_restaurant_authentication_tokens(restaurant)
                save_restaurant_auth_tokens(authentication_tokens)
               
                return GenericSuccessResponse(authentication_tokens, message=USER_LOGGED_IN_SUCCESSFULLY)
           
            else:
                return CustomBadRequest(message=INCORRECT_PASSWORD)

        except RestaurantProfile.DoesNotExist:
            return CustomBadRequest(message=WRONG_EMAIL)
       
        except Exception as e:
            return GenericException(traceback)


class ResetPassword(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    @staticmethod
    def patch(request):
        try:
            restaurant = request.user

            if "new_password1" not in request.data or "new_password2" not in request.data:
                raise CustomBadRequest(message=BAD_REQUEST)
            
            new_password1 = request.data["new_password1"]
            new_password2 = request.data["new_password2"]

           
            del request.data["new_password1"]
            del request.data["new_password2"]


            resetpassword_serializer = ResetPasswordSerializer(data=request.data)
           
            if "password" not in request.data:
                raise CustomBadRequest(message=BAD_REQUEST)
           
            else:
                restaurant = RestaurantProfile.objects.get(email=restaurant.email, is_deleted=False)
           
                if check_password(request.data["password"], restaurant.password):
           
                    if new_password1 == new_password2:
           
                        if validate_password(new_password2):
                            request.data["password"] = make_password(new_password1)
           
                            if resetpassword_serializer.is_valid():
                                resetpassword_serializer.update(restaurant, resetpassword_serializer.validated_data)
           
                                return GenericSuccessResponse('e', message=YOUR_PASSWORD_UPDATED_SUCCESSFULLY)
           
                    else:
                        return CustomBadRequest(message=NEW_PASSWORD_DOESNT_MATCH)
           
                else:
                    return CustomBadRequest(message=INCORRECT_PASSWORD)

        except Exception as e:
            return GenericException(traceback)


class OTPVerification(APIView):
    @staticmethod
    def post(request):
        try:
            if "email" not in request.data:
                raise CustomBadRequest(message=BAD_REQUEST)
       
            email = request.data["email"]
            otp = str(random.randint(1000, 9999))
            request.data["otp"] = otp
       
            del request.data["email"]

            restaurant = RestaurantProfile.objects.get(email=email, is_deleted=False)
            request.data["restaurant_id"] = restaurant.restaurant_id
          
            otpverification_serializer = OTPVerificationSerializer(data=request.data)

            if otpverification_serializer.is_valid():
                otpverification_serializer.save()
                send_mail([email], msg=otp)
               
                return GenericSuccessResponse("e", message=OTP_SENT_SUCCESSFULLY)


        except RestaurantProfile.DoesNotExist:
            return CustomBadRequest(message=WRONG_EMAIL)
       
        except Exception as e:
            return GenericException(traceback)


class ForgotPassword(APIView):
    @staticmethod
    def patch(request):
        try:
            if "email" not in request.data or "new_password1" not in request.data or "new_password2" not in request.data or "otp" not in request.data:
                raise CustomBadRequest(message=BAD_REQUEST)
           
            new_password1 = request.data["new_password1"]
            new_password2 = request.data["new_password2"]
            email = request.data["email"]
            otp = request.data["otp"]
           
            del request.data["new_password1"]
            del request.data["new_password2"]
            del request.data["email"]
            del request.data["otp"]

            resetpassword_serializer = ResetPasswordSerializer(data=request.data)
            restaurant = RestaurantProfile.objects.get(email=email, is_deleted=False)
            restaurant_otp = RestaurantOTP.objects.filter(restaurant_id=restaurant.restaurant_id).last()
            
            if new_password1 == new_password2:
            
                if (datetime.datetime.now(pytz.UTC) - restaurant_otp.created_at < datetime.timedelta(minutes=2)):
            
                    if restaurant_otp.otp == otp:
            
                        if validate_password(new_password2):
                            request.data["password"] = make_password(new_password1)
            
                            if resetpassword_serializer.is_valid():
                                resetpassword_serializer.update(restaurant, resetpassword_serializer.validated_data)
            
                                return GenericSuccessResponse('e', message=YOUR_PASSWORD_UPDATED_SUCCESSFULLY)
            
                    else:
                        return CustomBadRequest(message=OTP_DOESNT_MATCH)
            
                else:
                    return CustomBadRequest(message=OTP_EXPIRED)
            
            else:
                return CustomBadRequest(message=NEW_PASSWORD_DOESNT_MATCH)

        except Exception as e:
            return GenericException()



class GetRestaurantType(APIView):
    @staticmethod
    def get(request):
        try:
            restaurant_type_choices = RestaurantType.choices()
            response = {choice[0]: choice[1] for choice in restaurant_type_choices}
            print(response)
            return GenericSuccessResponse(response)
        except:
            GenericException()
        
