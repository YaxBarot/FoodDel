import json


from offers.models import Offers
from offers.serializers import OffersSerializer
from restaurant.models import RestaurantProfile
from customer.serializers import CartSerializer, JSONMenuSerializer, RegistrationSerializer
from restaurant.serializers import RegistrationSerializer as RestrauntRegistrationSerializer
from exceptions.generic_response import GenericSuccessResponse
from menu.serializers import MenuItemSerializer
from exceptions.generic import CustomBadRequest
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from security.customer_authorization import CustomerJWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers

from exceptions.generic import GenericException
from menu.models import MenuItem

from customer.models import Cart, Customers

from customer.serializers import ShowCartSerializer


class AddToCart(APIView):
    authentication_classes = [CustomerJWTAuthentication]



    def patch(self, request):
        try:
            customer = request.user
            request.data["id"] = customer.id

            if "menu_id" not in request.data :
                return CustomBadRequest(message="Menu ID is required")
            if "quantity" not in request.data:
                request.data["quantity"]=1
            cart = Cart.objects.filter(id=request.data["id"]).first()
            
            if cart.menu_item.get(str(request.data["menu_id"])):
                menu_item = MenuItem.objects.get(menu_id=request.data["menu_id"])
                if request.data["quantity"] == 0:   
                    value = cart.menu_item.pop(str(request.data["menu_id"]))
                    request.data["menu_item"] = cart.menu_item
                   
                else:
                    cart.menu_item[str(request.data["menu_id"])]["quantity"] = request.data["quantity"]
                    request.data["menu_item"] = cart.menu_item
                
                total_price = 0
              
                for value in cart.menu_item.items():  
                    price = float(value[1]["price"])
                    quantity = int(value[1]["quantity"])
                    total_price += price * quantity
                
                request.data["total_price"] = total_price
                request.data["restaurant_id"] = menu_item.restaurant_id.restaurant_id
                del request.data["quantity"]
                
                cart_serializer = CartSerializer(data=request.data)
                
                if cart_serializer.is_valid(raise_exception=True):
                    cart = cart_serializer.update(cart,cart_serializer.validated_data) 
                    serialized_cart = CartSerializer(cart)
                    
                    return GenericSuccessResponse(serialized_cart.data)
           
            else:
                menu_item = MenuItem.objects.get(menu_id=request.data["menu_id"])
                
                json_dict = {
                    "restaurant_id": menu_item.restaurant_id.restaurant_id,
                    "category_id": menu_item.category_id.category_id,
                    "menu_id": menu_item.menu_id,
                    "name": menu_item.name,
                    "description": menu_item.description,
                    "price": float(menu_item.price),
                    "quantity": int(request.data["quantity"]),
                    "item_pic": menu_item.item_pic
                }

                json_menu_serializer_data = JSONMenuSerializer(json_dict)
                
                cart.menu_item[json_menu_serializer_data.data['menu_id']] = json_menu_serializer_data.data
                
                total_price = 0
                
                for value in cart.menu_item.items():
                    total_price  = total_price + float(value[1]["price"]) * int(value[1]["quantity"])

                request.data["total_price"] = total_price
                request.data["restaurant_id"] = menu_item.restaurant_id.restaurant_id
                del request.data["menu_id"]
                del request.data["quantity"]
                request.data["menu_item"] = cart.menu_item
                
                cart_serializer = CartSerializer(data=request.data)

                if cart_serializer.is_valid(raise_exception=True):
                    cart = cart_serializer.update(cart, cart_serializer.validated_data)
                    serialized_cart = CartSerializer(cart)
                   
                    return GenericSuccessResponse(serialized_cart.data)
               
                else:
                    return CustomBadRequest(message="Invalid data")


        except MenuItem.DoesNotExist:
            return CustomBadRequest(message="Menu item not found")

        except ValidationError as e:
            return CustomBadRequest(message=e.detail)

        except Exception as e:

            return CustomBadRequest(message="An error occurred")

    


class DeleteInCart(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    def delete(self, request, cart_id):
        try:
            cart_item = Cart.objects.get(customer_cart_id=cart_id)
            cart_item.delete()
            return GenericSuccessResponse({"message": "Cart item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Cart.DoesNotExist:
            return GenericSuccessResponse({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:

            return GenericSuccessResponse({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCart(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    def get(self, request):
        try:
            customer = request.user
            cart_items = Cart.objects.filter(id=customer.id)
            
            show_cart_serializer = ShowCartSerializer(cart_items, many=True)

            return Response(show_cart_serializer.data)

        except Exception as e:

            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class Cartcheckout(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    def patch(self, request):
        try:
            customer = request.user
            request.data["id"] = customer.id

            if "customer_cart_id" not in request.data:
                return CustomBadRequest(message="customer_cart_id is not in request.data")

            cart = Cart.objects.get(customer_cart_id=request.data["customer_cart_id"])
            total_price = cart.total_price

            customer = Customers.objects.get(id=request.data["id"])
          
            new_customer_credit = float(customer.credit) - float(total_price)
            customer.credit = new_customer_credit

            registration_serializer = RegistrationSerializer(customer, data=request.data, partial=True)


            if registration_serializer.is_valid():

                registration_serializer.save()

                return Response({"message": "Restaurant and custommer credit and order status updated successfully"}, status=status.HTTP_200_OK)


        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except Customers.DoesNotExist:
            return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ApplyOffer(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    def get(self, request, restaurant_id):
        try:

            offers = Offers.objects.filter(restaurant_id=restaurant_id, is_approved=True)

            if offers.exists():
                offers_serializer = OffersSerializer(offers, many=True)
                return GenericSuccessResponse(offers_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "offer not found"}, status=status.HTTP_404_NOT_FOUND)

        except Offers.DoesNotExist:
            return Response({"message": "offer not found"}, status=status.HTTP_404_NOT_FOUND)
    
        except Exception as e:
            return GenericException(str(e))
        


