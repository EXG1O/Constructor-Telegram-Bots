from django.urls import path, include

from .views import UserAPIView, UserLoginAPIView, UserLogoutAPIView


urlpatterns = [
	path('user/', include([
		path('', UserAPIView.as_view()),
		path('login/', UserLoginAPIView.as_view()),
		path('logout/', UserLogoutAPIView.as_view()),
	])),
]