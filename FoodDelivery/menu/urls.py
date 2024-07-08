from django.urls import path
from .views import MenuCategoryCreate, MenuCategoryUpdate, MenuCategoryDelete, MenuItemCreate, MenuItemUpdate, \
    MenuItemDelete, MenuItemavailablity

urlpatterns = [
    path('createcategory/', MenuCategoryCreate.as_view()),
    path('updatecategory/<int:category_id>/', MenuCategoryUpdate.as_view()),
    path('deletecategory/<int:category_id>/', MenuCategoryDelete.as_view()),
    path('createiteam/', MenuItemCreate.as_view()),
    path('updateiteam/<int:menu_id>/', MenuItemUpdate.as_view()),
    path('deleteiteam/<int:menu_id>/', MenuItemDelete.as_view()),
    path('menuitemavailablity/<int:menu_id>/', MenuItemavailablity.as_view())

]

