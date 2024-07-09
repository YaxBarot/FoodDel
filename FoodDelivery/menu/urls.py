from django.urls import path
from .views import MenuCategoryCreate, MenuCategoryUpdate, MenuCategoryDelete, MenuItemCreate, MenuItemUpdate, \
    MenuItemDelete, MenuItemavailablity

urlpatterns = [
    path('createcategory/', MenuCategoryCreate.as_view()),
    path('updatecategory/<int:category_id>/', MenuCategoryUpdate.as_view()),
    path('deletecategory/<int:category_id>/', MenuCategoryDelete.as_view()),
    path('createitem/', MenuItemCreate.as_view()),
    path('updateitem/<int:menu_id>/', MenuItemUpdate.as_view()),
    path('deleteitem/<int:menu_id>/', MenuItemDelete.as_view()),
    path('menuitemavailablity/<int:menu_id>/', MenuItemavailablity.as_view())

]

