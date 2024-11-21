from rest_framework.routers import SimpleRouter

from .views import DonationViewSet, MethodViewSet, SectionViewSet

router = SimpleRouter(use_regex_path=False)
router.register('donations', DonationViewSet, basename='donation')
router.register('sections', SectionViewSet, basename='section')
router.register('methods', MethodViewSet, basename='method')

app_name = 'donation'
urlpatterns = router.urls
