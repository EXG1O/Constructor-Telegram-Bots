from rest_framework.routers import SimpleRouter

from .views import SectionsViewSet

router = SimpleRouter()
router.register('sections', SectionsViewSet, basename='section')

app_name = 'privacy-policy'
urlpatterns = router.urls
