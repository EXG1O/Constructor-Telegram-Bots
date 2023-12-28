from django.urls import path

from .views import InstructionSectionsAPIView


app_name = 'instruction'
urlpatterns = [
	path('sections/', InstructionSectionsAPIView.as_view(), name='sections'),
]