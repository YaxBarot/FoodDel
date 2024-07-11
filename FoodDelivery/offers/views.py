import traceback
from customer.serializers import CartSerializer
from security.administration_authorization import AdministratorJWTAuthentication
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from .models import Offers
from .serializers import OffersApprovalSerializer, OffersSerializer

from exceptions.generic import CustomBadRequest, BadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse
from security.restaurant_authorization import RestaurantJWTAuthentication
from security.customer_authorization import CustomerJWTAuthentication
from common.constants import BAD_REQUEST, OFFER_UNAVAILABLE, ONE_PROMOTION_ALLOWED, WE_COULDNT_APPLY_THE_PROMOTION, \
    ALREADY_APPLIED, ORDER_HAS_ALREADY_BEEN_PLACED
from customer.models import Cart, OffersHistory


class OffersCreate(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    def post(self, request):
        try:
            restaurant = request.user
            request.data["restaurant_id"] = restaurant.restaurant_id
            serializer = OffersSerializer(data=request.data)

            
            
            if "type" not in request.data or not str(request.data["type"]).strip():
                return CustomBadRequest(message="type is required")
            
            else:
                if request.data["type"] == "ON_CART":
                   
                    if "discount" not in request.data:
                        return CustomBadRequest(message="discount is not optional field for type ON_CART")
                    
                    if "discount" in request.data  and "item_id" in request.data: 
                        return CustomBadRequest(message="Can not accept discount and item_id at a same time with ON_CART type")

                if request.data["type"] == "ON_ITEM":
                                            
                    if "discount" in request.data  and "free_item" in request.data: 
                        return CustomBadRequest(message="Can not accept discount and free_item at a same time")
                   
                    if "discount" not in request.data:

                        if "item_id" not in request.data or "item_quantity" not in request.data:
                            return CustomBadRequest(message="item_id or item_quantity is missing")
                        
                        if "free_item" not in request.data:
                            return CustomBadRequest(message="Need to enter one of the field from discount or free_item")
    
                        
                    if "free_item" in request.data and "free_item_quantity" not in request.data:
                        return  CustomBadRequest(message="free_item_quantity is missing")
                        

            if "item_id" in request.data and "discount" not in request.data and Offers.objects.filter(type=request.data["type"], item_id=request.data["item_id"]).exists() :
                return CustomBadRequest(message="An offer with this item and type already exists")

            else:

                if serializer.is_valid(raise_exception=True):
                    offer = serializer.save()
                    return GenericSuccessResponse({'offer_id': offer.offer_id, 'type': offer.type},
                                                  message="Offer created successfully")
                else:
                    return CustomBadRequest(message="Invalid data")

        except ValidationError as e:
            return CustomBadRequest(message=e.detail)
        except Exception as e:
            traceback.print_exc()
            return GenericException()


class OffersDelete(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    def delete(self, request, offer_id):
        try:
            offer = Offers.objects.get(offer_id=offer_id)

            offer.is_deleted = True
            offer_serializer = OffersSerializer(offer, data={"is_deleted": offer.is_deleted}, partial=True)
            if offer_serializer.is_valid():
                offer_serializer.save()
                return Response({"message": "offer deleted successfully"}, status=status.HTTP_200_OK)

        except Offers.DoesNotExist:
            return CustomBadRequest(message="Offer not found")

        except Exception as e:
            return GenericException()


class OffersApproval(APIView):
    authentication_classes = [AdministratorJWTAuthentication]

    def get(self, request, offer_id):
        try:

            offer = Offers.objects.get(offer_id=offer_id)

            offers_serializer = OffersSerializer(offer)

            return GenericSuccessResponse(offers_serializer.data, status=status.HTTP_200_OK)

        except Offers.DoesNotExist:
            return Response({"message": "offer not found"}, status=status.HTTP_404_NOT_FOUND)

        except:
            GenericException()

    def patch(self, request, offer_id):
        try:

            if "offer_id" not in request.data or "is_approved" not in request.data:
                raise CustomBadRequest(message="BAD_REQUEST")

            offer = Offers.objects.get(offer_id=request.data["offer_id"])

            offer.is_approved = request.data["is_approved"]
            offer_approval_serializer = OffersApprovalSerializer(data=request.data)

            if offer_approval_serializer.is_valid():
                offer = offer_approval_serializer.update(offer, offer_approval_serializer.validated_data)
                return Response(offer_approval_serializer.data, status=status.HTTP_200_OK)


        except Offers.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CustomBadRequest as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return GenericException()


class ApplyPromotions(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def patch(request):
        try:
            if "offer_id" not in request.data or "customer_cart_id" not in request.data:
                return CustomBadRequest(message="Bad request: Missing offer_id or customer_cart_id.")

            cart = Cart.objects.get(customer_cart_id=request.data["customer_cart_id"])
            offer = Offers.objects.get(offer_id=request.data["offer_id"])

            if cart.restaurant_id != offer.restaurant_id:
                return CustomBadRequest(message="Offer is unavailable for this restaurant.")

            if cart.is_offer_applied and not offer.allow_multiple_offers:
                return CustomBadRequest(message="Only one promotion is allowed per cart.")

            if OffersHistory.objects.filter(offers_id=offer.offer_id, cart_id=cart.customer_cart_id).exists():
                return CustomBadRequest(message="Offer has already been applied.")

            if cart.is_ordered:
                return CustomBadRequest(message="Order has already been placed.")

            if offer.type == "ON_CART":
                cart.discounted_price = float(cart.total_price) * (1-float(offer.discount) / 100)
                cart.is_offer_applied = True
                cart.save()
                return GenericSuccessResponse(CartSerializer(cart).data, message="Offer applied successfully.")
            else:
                if offer.discount != 0:
                    if str(offer.item_id.menu_id) in cart.menu_item:
                        cart.discounted_price = float(cart.total_price) - int(cart.menu_item[str(offer.item_id.menu_id)]["quantity"]) * float(cart.menu_item[str(offer.item_id.menu_id)]["price"]) * (offer.discount / 100)
                        cart.is_offer_applied = True
                        cart.save()
                        return GenericSuccessResponse(CartSerializer(cart).data, message="Offer applied successfully.")
                    else:
                        return CustomBadRequest(message="Offer not applicable to cart items.")
                else:
                    if str(offer.item_id.menu_id) in cart.menu_item and str(offer.free_item.menu_id) in cart.menu_item:
                        cart_item_quantity = int(cart.menu_item[str(offer.item_id.menu_id)]["quantity"])
                        cart_free_item_quantity = int(cart.menu_item[str(offer.free_item.menu_id)]["quantity"])

                        cart.discounted_price = cart.total_price

                        if offer.item_id == offer.free_item:
                            if int(offer.free_item_quantity) + int(offer.item_quantity) > cart_item_quantity :
                                return CustomBadRequest(message="conditions are not satisfied for this promotion")
                        
                        while cart_item_quantity >= int(offer.item_quantity) and cart_free_item_quantity >= int(offer.free_item_quantity):
                            cart.discounted_price = float(cart.discounted_price) - offer.free_item_quantity * float(cart.menu_item[str(offer.free_item.menu_id)]["price"])
                            print("cart.discounted_price",cart.discounted_price)
                            print("cart_free_item_quantity",cart_free_item_quantity)
                            print("float(cart.menu_item[str(offer.free_item.menu_id)]['price'])",float(cart.menu_item[str(offer.free_item.menu_id)]["price"]))
                            if offer.item_id == offer.free_item:

                                cart_item_quantity = cart_item_quantity - offer.item_quantity - offer.free_item_quantity
                                cart_free_item_quantity = cart_free_item_quantity - offer.free_item_quantity - offer.item_quantity

                            else:

                                cart_item_quantity = cart_item_quantity - offer.item_quantity
                                cart_free_item_quantity = cart_free_item_quantity - offer.free_item_quantity
                            

                        cart.is_offer_applied = True
                        cart.save()
                        return GenericSuccessResponse(CartSerializer(cart).data, message="Offer applied successfully.")
                    else:
                        return CustomBadRequest(message="Offer not applicable to cart items.")

        except Offers.DoesNotExist:
            return CustomBadRequest(message="Offer does not exist.")
        except Cart.DoesNotExist:
            return CustomBadRequest(message="Cart does not exist.")
        except Exception as e:
            traceback.print_exc()
            return GenericException()