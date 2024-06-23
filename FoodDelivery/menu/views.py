from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import MenuCategory
from .serializers import MenuCategorySerializer
from exceptions.generic import CustomBadRequest, BadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse


class MenuCategoryCreate(APIView):

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
            return GenericException()


