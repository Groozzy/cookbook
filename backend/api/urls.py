from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register('tags', views.TagViewSet, 'tags')
router.register('ingredients', views.IngredientViewSet, 'ingredients')
router.register('recipes', views.RecipeViewSet, 'recipes')
router.register('users', views.UserViewSet, 'users')

urlpatterns = (path('', include(router.urls)),
               path('auth/', include('djoser.urls.authtoken')))
