from rest_framework.routers import SimpleRouter

from .views import SectionViewSet

router = SimpleRouter()
router.register('sections', SectionViewSet, basename='section')

app_name = 'instruction'
urlpatterns = router.urls
