
from exceptions.generic import CustomBadRequest, BadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse

from security.restaurant_authorization import RestaurantJWTAuthentication

from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .models import Offers
from .serializers import OffersSerializer
from rest_framework import status
from rest_framework.response import Response


class OffersCreate(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    def post(self, request):
        try:
            serializer = OffersSerializer(data=request.data)

            if "type" not in request.data or not str(request.data["type"]).strip():
                return CustomBadRequest(message="type is required")

            if Offers.objects.filter(type=request.data["type"]).exists():
                return CustomBadRequest(message="An offer with this item and type already exists")

            if Offers.objects.filter(type=request.data["item_id"]).exists():
                return CustomBadRequest(message="An offer with this item and type already exists")

            if serializer.is_valid(raise_exception=True):
                offer = serializer.save()
                return GenericSuccessResponse({'offer_id': offer.offer_id, 'type': offer.type},
                                              message="Offer created successfully")
            else:
                return CustomBadRequest(message="Invalid data")
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
