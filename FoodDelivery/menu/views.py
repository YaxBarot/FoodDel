from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import MenuCategory, MenuItem
from .serializers import MenuCategorySerializer, MenuItemSerializer
from exceptions.generic import CustomBadRequest, BadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse

from security.restaurant_authorization import RestaurantJWTAuthentication


class MenuCategoryCreate(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    def post(self, request):
        try:
            serializer = MenuCategorySerializer(data=request.data)

            if "name" not in request.data or not request.data["name"].strip():
                return CustomBadRequest(message="Name is required")

            if MenuCategory.objects.filter(name=request.data["name"]).exists():
                return CustomBadRequest(message="Category with this name already exists")

            if serializer.is_valid(raise_exception=True):
                menu_category = serializer.save()
                return GenericSuccessResponse({'category_id': menu_category.category_id, 'name': menu_category.name}, message="Category created successfully")
            else:
                return CustomBadRequest(message="Invalid data")
        except ValidationError as e:
            return CustomBadRequest(message=e.detail)
        except Exception as e:
            print(f"An error occurred: {e}")
            return GenericException()


class MenuCategoryUpdate(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    def patch(self, request,category_id):
        try:
            try:
                menu_category = MenuCategory.objects.get(category_id=category_id)
            except MenuCategory.DoesNotExist:
                return CustomBadRequest(message="Category not found")

            serializer = MenuCategorySerializer(menu_category, data=request.data, partial=True)

            if "name" in request.data and not request.data["name"].strip():
                return CustomBadRequest(message="Name cannot be empty")

            if "name" in request.data and MenuCategory.objects.filter(name=request.data["name"]).exclude(category_id=category_id).exists():
                return CustomBadRequest(message="Category with this name already exists")

            if serializer.is_valid(raise_exception=True):
                menu_category = serializer.save()
                return GenericSuccessResponse({'category_id': menu_category.category_id, 'name': menu_category.name}, message="Category updated successfully")
            else:
                return CustomBadRequest(message="Invalid data")
        except ValidationError as e:
            return CustomBadRequest(message=e.detail)
        except Exception as e:
            print(f"An error occurred: {e}")
            return GenericException()

class MenuCategoryDelete(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    def delete(self, request, category_id):
        try:
            menu_category = MenuCategory.objects.get(category_id=category_id)
        except MenuCategory.DoesNotExist:
            return CustomBadRequest(message="Category not found")

        try:
            menu_category.delete()
            return GenericSuccessResponse(message="Category deleted successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
            return GenericException()
        
class MenuItemCreate(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    def post(self, request):
        try:
            restaurant = request.user
            request.data["restaurant_id"] = restaurant.restaurant_id
            menu_serializer = MenuItemSerializer(data=request.data)

            if "name" not in request.data or not request.data["name"].strip():
                return CustomBadRequest(message="Name is required")

            if MenuItem.objects.filter(name=request.data["name"]).exists():
                return CustomBadRequest(message="Item with this name already exists")

            if menu_serializer.is_valid(raise_exception=True):
                menu_item = menu_serializer.save()
                return GenericSuccessResponse({'item_id': menu_item.menu_id, 'name': menu_item.name}, message="Item created successfully")
            else:
                return CustomBadRequest(message="Invalid data")
        except ValidationError as e:
            return CustomBadRequest(message=e.detail)
        except Exception as e:
            print(f"An error occurred: {e}")
            return GenericException()

class MenuItemUpdate(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    def patch(self, request, menu_id):
        try:
            restaurant = request.user
            request.data["restaurant_id"] = restaurant.restaurant_id
            menu_item = MenuItem.objects.get(id=menu_id)
            menu_serializer = MenuItemSerializer(instance=menu_item, data=request.data)

            if menu_serializer.is_valid(raise_exception=True):
                menu_serializer.save()
                return GenericSuccessResponse({'item_id': menu_item.menu_id, 'name': menu_item.name}, message="Item updated successfully")
            else:
                return CustomBadRequest(message="Invalid data")
        except MenuItem.DoesNotExist:
            return CustomBadRequest(message="Item not found")
        except ValidationError as e:
            return CustomBadRequest(message=e.detail)
        except Exception as e:
            print(f"An error occurred:{e}")
            return GenericException()

class MenuItemDelete(APIView):
    authentication_classes = [RestaurantJWTAuthentication]

    def delete(self, request, menu_id):
        try:
            menu_item = MenuItem.objects.get(menu_id=menu_id)
            menu_item.delete()
            return GenericSuccessResponse(message="Item deleted successfully")
        except MenuItem.DoesNotExist:
            return CustomBadRequest(message="Item not found")
        except Exception as e:
            print(f"An error occurred: {e}")
            return GenericException()
