from django.urls import path, include

from .views import UserAPIView, UserLoginAPIView, UserLogoutAPIView


app_name = 'users'
urlpatterns = [
	path('_/', include(((
		path('', UserAPIView.as_view(), name='index'),
		path('login/', UserLoginAPIView.as_view(), name='login'),
		path('logout/', UserLogoutAPIView.as_view(), name='logout'),
	), 'detail'))),
]