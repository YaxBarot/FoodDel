from rest_framework.views import APIView

from .models import RatingHistory
from .serializers import RatingHistorySerializer

from security.customer_authorization import CustomerJWTAuthentication
from exceptions.generic import CustomBadRequest, BadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse
from common.constants import BAD_REQUEST, NO_SUCH_RESTAURANT_EXISTS, RATING_CANNOT_BE_GIVEN, ONE_RATING_ALLOWED, \
    RATING_GIVEN_SUCCESSFULLY
from restaurant.models import RestaurantProfile
from customer.models import Cart


class RateRestaurant(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def post(request):
        try:
            current_customer = request.user

            request.data["customer_id"] = current_customer.id

            if "restaurant_id" not in request.data or "rating" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)

            if RatingHistory.objects.filter(customer_id=current_customer.id,
                                            restaurant_id=request.data["restaurant_id"], is_deleted=False).exists():
                return CustomBadRequest(message=ONE_RATING_ALLOWED)

            Cart.objects.get(id=current_customer.id, is_deleted=False, is_ordered=True)
            restaurant = RestaurantProfile.objects.get(restaurant_id=request.data["restaurant_id"], is_deleted=False)

            new_rating = (restaurant.rating + request.data["rating"]) / (restaurant.no_of_ratings + 1)
            restaurant.rating = new_rating
            restaurant.no_of_ratings += 1
            restaurant.save()

            rating_history_serializer = RatingHistorySerializer(data=request.data)

            if rating_history_serializer.is_valid():
                rating_history_serializer.save()

            return GenericSuccessResponse(message=RATING_GIVEN_SUCCESSFULLY)

        except Cart.DoesNotExist:
            return CustomBadRequest(message=RATING_CANNOT_BE_GIVEN)

        except RestaurantProfile.DoesNotExist:
            return CustomBadRequest(message=NO_SUCH_RESTAURANT_EXISTS)

        except Exception as e:
            return GenericException()
