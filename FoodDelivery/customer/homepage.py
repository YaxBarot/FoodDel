
import traceback
from common.constants import BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response

from restaurant.models import RestaurantProfile, RestaurantType
from security.customer_authorization import CustomerJWTAuthentication
from exceptions.generic_response import GenericSuccessResponse
from exceptions.generic import CustomBadRequest, GenericException
from .serializers import RestaurantListSerializer


class ShowRestaurantList(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def get(request,restaurant_type):
        try:

            if restaurant_type=="ALL_TYPES":
                restaurant_list = RestaurantProfile.objects.filter(operational_status=True)
                closed_restaurant_list = RestaurantProfile.objects.filter(operational_status=False)
     
            else:
                restaurant_list = RestaurantProfile.objects.filter(Restaurant_type=restaurant_type, operational_status=True)
                closed_restaurant_list = RestaurantProfile.objects.filter(operational_status=False,Restaurant_type=restaurant_type)


            restaurant_list = restaurant_list | closed_restaurant_list
            

            restraunt_serializer = RestaurantListSerializer(restaurant_list, many=True)

            response = {}
            
            
            for i in restraunt_serializer.data:
                      
                response[str(i["restaurant_id"])] = i

            return GenericSuccessResponse(response)
        except Exception as e:

            return GenericException()


class GetRestaurantType(APIView):


    @staticmethod

    def get(request):

        types = RestaurantType.choices()
        return GenericSuccessResponse(types)

