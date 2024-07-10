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

            if Offers.objects.filter(type=request.data["type"], item_id=request.data["item_id"]).exists():
                return CustomBadRequest(message="An offer with this item and type already exists")

            if Offers.objects.filter(item_id__restaurant_id=restaurant.restaurant_id).exists():

                if serializer.is_valid(raise_exception=True):
                    offer = serializer.save()
                    return GenericSuccessResponse({'offer_id': offer.offer_id, 'type': offer.type},
                                                  message="Offer created successfully")
                else:
                    return CustomBadRequest(message="Invalid data")
            else:
                return CustomBadRequest(message="this item doesnt belongs to your restaurant")
        except ValidationError as e:
            return CustomBadRequest(message=e.detail)
        except Exception as e:
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
    # authentication_classes = [AdministratorJWTAuthentication]

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
            if "offer_id" not in request.data or "cart_id" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)

            cart = Cart.objects.get(cart_id=request.data["cart_id"])
            offer = Offers.objects.get(offer_id=request.data["offer_id"])

            if cart.restaurant_id != offer.restaurant_id:
                return CustomBadRequest(message=OFFER_UNAVAILABLE)

            if cart.is_offer_applied and not offer.allow_multiple_offers:
                return CustomBadRequest(message=ONE_PROMOTION_ALLOWED)

            if OffersHistory.objects.filter(offers_id=offer.offer_id, cart_id=cart.cart_id).exists():
                return CustomBadRequest(message=ALREADY_APPLIED)

            if cart.is_ordered:
                return CustomBadRequest(message=ORDER_HAS_ALREADY_BEEN_PLACED)

            if offer.type == "ON_CART":
                cart.total_price = cart.total_price * (offer.discount / 100)
                cart.is_offer_applied = True
                cart.save()

            else:
                pass

        except Offers.DoesNotExist:
            return CustomBadRequest(message=OFFER_UNAVAILABLE)

        except Cart.DoesNotExist:
            return CustomBadRequest(message=WE_COULDNT_APPLY_THE_PROMOTION)

        except Exception as e:
            return GenericException()
