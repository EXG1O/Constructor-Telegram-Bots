from django.urls import path

from .views import LanguagesAPIView

app_name = 'languages'
urlpatterns = [path('', LanguagesAPIView.as_view(), name='index')]
