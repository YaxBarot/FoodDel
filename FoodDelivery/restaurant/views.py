from django.shortcuts import render
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.db.models import Q
from customer.serializers import CartSerializer
from customer.models import Cart, Customers
from security.customer_authorization import CustomerJWTAuthentication
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

from .serializers import CartItemSerializer, OperationalStatusSerializer, RegistrationSerializer, ResetPasswordSerializer, OTPVerificationSerializer



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
          
            return GenericSuccessResponse(response)        
        except:
            GenericException()
        
class OperationalStatus(APIView):

    authentication_classes = [RestaurantJWTAuthentication]

    def get(self, request):
        try:
            restaurant = request.user

            restaurant = RestaurantProfile.objects.get(restaurant_id=restaurant.restaurant_id)

            operational_status_serializer = OperationalStatusSerializer(restaurant)

            return GenericSuccessResponse(data=operational_status_serializer.data)
        except RestaurantProfile.DoesNotExist:
            return Response({"message": "RestaurantProfile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return GenericException()


    def patch(self, request):
        try:
            restaurant = request.user

            if "operational_status" not in request.data:
                raise CustomBadRequest(message="BAD_REQUEST")
            
            operational_status_serializer = OperationalStatusSerializer(data=request.data)
            restaurant = RestaurantProfile.objects.get(restaurant_id=restaurant.restaurant_id)

            print(restaurant)
            print(request.data)
            print(operational_status_serializer)    

            if operational_status_serializer.is_valid():
                print("Valid data received")
                operational_status_serializer.update(restaurant, operational_status_serializer.validated_data)
              
                return GenericSuccessResponse('e', message="Your operational status has been updated successfully.")
            
            else:
                return Response(operational_status_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except:
            GenericException()




class CartApproval(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    
    def get(self, request):
        try:

            if "customer_cart_id" not in request.data:
                raise CustomBadRequest(message="BAD_REQUEST")
       
            cart = Cart.objects.get(customer_cart_id = request.data["customer_cart_id"])
  
            cart_request_dict={}
            cart_request_dict = {
                    "restaurant_id": cart.restaurant_id.restaurant_id,
                    "id": cart.id.id,
                    "menu_item": cart.menu_item,
                    "total_price": cart.total_price,
                    "is_ordered": cart.is_ordered,
                   
                }

            cart_serializer = CartItemSerializer(cart_request_dict)
                
            return Response(cart_serializer.data, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
    
        except:
            GenericException()
        

    def patch(self, request):
        try:
            restaurant = request.user


            if "customer_cart_id" not in request.data or "is_approved" not in request.data:
                raise CustomBadRequest(message="BAD_REQUEST")

            cart = Cart.objects.get(customer_cart_id=request.data["customer_cart_id"], restaurant_id=restaurant.restaurant_id, is_deleted=False)

            if request.data["is_approved"] == 1:
                cart.is_ordered = True
                cart_serializer = CartSerializer(cart, data={"is_ordered": cart.is_ordered}, partial=True)

                restaurant = RestaurantProfile.objects.get(restaurant_id = cart.restaurant_id.restaurant_id)
                new_restaurant_credit =  float(restaurant.credit) + float(cart.total_price)
                restaurant.credit = new_restaurant_credit
                
                restaurant_serializer = RegistrationSerializer(restaurant,data = request.data, partial=True)

                cart.is_ordered = True
                cart_serializer = CartSerializer(cart,data = request.data, partial=True)
                
                if restaurant_serializer.is_valid() and cart_serializer.is_valid():
                    restaurant_serializer.save()
                    cart_serializer.save()
                    return Response(cart_serializer.data, status=status.HTTP_200_OK)
                    
            else:
                cart.is_deleted = True
                cart_serializer = CartSerializer(cart, data={"is_deleted": cart.is_deleted}, partial=True)

                total_price = cart.total_price

                customer = Customers.objects.get(id=cart.id.id)

                new_customer_credit = float(customer.credit) + float(total_price)
                customer.credit = new_customer_credit

                registration_serializer = RegistrationSerializer(customer, data=request.data, partial=True)
                if registration_serializer.is_valid() and cart_serializer.is_valid() :

                    registration_serializer.save()
                    cart_serializer.save()  
                    return Response({"message": "custommer credit and order status updated successfully"}, status=status.HTTP_200_OK)

                
            
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CustomBadRequest as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return GenericException()
        
  