from django.urls import path, include

from .views import UsersAPIView, UserAPIView, UserLoginAPIView, UserLogoutAPIView


urlpatterns = [
	path('users/', UsersAPIView.as_view(), name='users'),
	path('user/', include([
		path('', UserAPIView.as_view(), name='user'),
		path('login/', UserLoginAPIView.as_view(), name='user-login'),
		path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
	])),
]