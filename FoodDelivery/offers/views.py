from django.shortcuts import render
#from security.administration_authorization import AdministratorJWTAuthentication
from exceptions.generic import CustomBadRequest, BadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse

from security.restaurant_authorization import RestaurantJWTAuthentication

from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .models import Offers
from .serializers import OffersApprovalSerializer, OffersSerializer
from rest_framework import status
from rest_framework.response import Response


class OffersCreate(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    def post(self, request):
        try:
            restaurant = request.user
            request.data["restaurant_id"] = restaurant.restaurant_id
            serializer = OffersSerializer(data=request.data)

            

            if "type" not in request.data or not str(request.data["type"]).strip():
                return CustomBadRequest(message="type is required")

            if Offers.objects.filter(type=request.data["type"],item_id=request.data["item_id"]).exists():
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
    #authentication_classes = [AdministratorJWTAuthentication]

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
            offer_approval_serializer = OffersApprovalSerializer(data = request.data)
   
            if offer_approval_serializer.is_valid():
                offer = offer_approval_serializer.update(offer,offer_approval_serializer.validated_data)
                return Response(offer_approval_serializer.data, status=status.HTTP_200_OK)
                
            
        except Offers.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CustomBadRequest as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return GenericException()
        
