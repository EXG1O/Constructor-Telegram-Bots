from django.urls import include, path

from .views import StatsAPIView, UserAPIView, UserLoginAPIView, UserLogoutAPIView

app_name = 'users'
urlpatterns = [
	path('stats/', StatsAPIView.as_view(), name='stats'),
	path(
		'_/',
		include(
			(
				(
					path('', UserAPIView.as_view(), name='index'),
					path('login/', UserLoginAPIView.as_view(), name='login'),
					path('logout/', UserLogoutAPIView.as_view(), name='logout'),
				),
				'detail',
			)
		),
	),
]
