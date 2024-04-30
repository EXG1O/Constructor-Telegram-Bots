from rest_framework.routers import SimpleRouter

from .views import UpdateViewSet

router = SimpleRouter(use_regex_path=False)  # type: ignore [call-arg]  # use_regex_path param exists
router.register('updates', UpdateViewSet, basename='update')

app_name = 'updates'
urlpatterns = router.urls
