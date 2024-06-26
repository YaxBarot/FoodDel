
from rest_framework.views import APIView
from rest_framework.response import Response

from restaurant.models import RestaurantProfile
from security.customer_authorization import CustomerJWTAuthentication
from exceptions.generic_response import GenericSuccessResponse
from exceptions.generic import GenericException
from .serializers import RestaurantListSerializer

class ShowRestaurantList(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def get(request):
        try:
            if 'Restaurant_type' in request.data and request.data['Restaurant_type']!='':
                restaurant_list = RestaurantProfile.objects.filter(Restaurant_type='RESTRAUNT').values()
           
            else:
                restaurant_list = RestaurantProfile.objects.all().values()

            restraunt_serializer = RestaurantListSerializer(restaurant_list, many=True)

            response = {}
            counter = 0
            
            for i in restraunt_serializer.data:
                      
                response["restraunt_"+ str(counter)] = i
                counter += 1

            return GenericSuccessResponse(response)
        except Exception as e:
            return GenericException()
            
