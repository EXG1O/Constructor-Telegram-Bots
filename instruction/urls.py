from django.urls import path

from .views import InstructionSectionsAPIView


urlpatterns = [
	path('sections/', InstructionSectionsAPIView.as_view(), name='instruction-sections'),
]