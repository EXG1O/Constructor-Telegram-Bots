from rest_framework.routers import SimpleRouter

from .views import UpdateViewSet

router = SimpleRouter(use_regex_path=False)
router.register('', UpdateViewSet, basename='update')

app_name = 'updates'
urlpatterns = router.urls
