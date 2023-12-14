from django.urls import path, include

from .views import UserLoginAPIView, UserLogoutAPIView, UsersAPIView, UserAPIView


urlpatterns = [
	path('user/', include([
		path('', UserAPIView.as_view(), name='user'),
		path('login/', UserLoginAPIView.as_view(), name='user-login'),
		path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
	])),
	path('users/', UsersAPIView.as_view(), name='users'),
]