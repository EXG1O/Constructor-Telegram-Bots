from rest_framework.routers import SimpleRouter

from .views import UpdateViewSet

router = SimpleRouter()
router.register('updates', UpdateViewSet, basename='update')

app_name = 'updates'
urlpatterns = router.urls
