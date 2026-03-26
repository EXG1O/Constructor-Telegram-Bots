from django.urls import path

from .routers import UserRouter
from .views import StatsAPIView, TokenViewSet, UserViewSet

user_router = UserRouter(use_regex_path=False)
user_router.register('', UserViewSet, basename='user')
user_router.register('tokens', TokenViewSet, basename='token')


app_name = 'users'
urlpatterns = [path('stats/', StatsAPIView.as_view(), name='stats')] + user_router.urls
