from django.urls import path

from .views import UserAPIView, UserLoginAPIView, UserLogoutAPIView


app_name = 'user'
urlpatterns = [
	path('', UserAPIView.as_view(), name='index'),
	path('login/', UserLoginAPIView.as_view(), name='login'),
	path('logout/', UserLogoutAPIView.as_view(), name='logout'),
]