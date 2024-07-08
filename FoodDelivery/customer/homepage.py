
from common.constants import BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response

from restaurant.models import RestaurantProfile
from security.customer_authorization import CustomerJWTAuthentication
from exceptions.generic_response import GenericSuccessResponse
from exceptions.generic import CustomBadRequest, GenericException
from .serializers import RestaurantListSerializer

class ShowRestaurantList(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def get(request):
        try:
            if 'Restaurant_type' in request.data :
                if request.data['Restaurant_type']!='':
                    restaurant_list = RestaurantProfile.objects.filter(Restaurant_type='RESTRAUNT', operational_status=True).values()
           
                else:
                    restaurant_list = RestaurantProfile.objects.filter(operational_status=True).values()

                closed_restrataunt_list = RestaurantProfile.objects.filter(operational_status=False).values()

                restaurant_list = restaurant_list | closed_restrataunt_list
                
            else:
                raise CustomBadRequest(message=BAD_REQUEST)
            

            restraunt_serializer = RestaurantListSerializer(restaurant_list, many=True)

            response = {}
            counter = 0
            
            for i in restraunt_serializer.data:
                      
                response["restraunt_"+ str(counter)] = i
                counter += 1

            return GenericSuccessResponse(response)
        except Exception as e:
            return GenericException()
            
