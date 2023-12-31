from django.urls import path, include

from .views import UsersAPIView, UserAPIView, UserLoginAPIView, UserLogoutAPIView


urlpatterns = [
	path('users/', UsersAPIView.as_view()),
	path('user/', include([
		path('', UserAPIView.as_view()),
		path('login/', UserLoginAPIView.as_view()),
		path('logout/', UserLogoutAPIView.as_view()),
	])),
]