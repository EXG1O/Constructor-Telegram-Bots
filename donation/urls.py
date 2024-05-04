from rest_framework.routers import SimpleRouter

from .views import ButtonViewSet, DonationViewSet, SectionViewSet

router = SimpleRouter(use_regex_path=False)  # type: ignore [call-arg]  # use_regex_path param exists
router.register('donations', DonationViewSet, basename='donation')
router.register('sections', SectionViewSet, basename='section')
router.register('buttons', ButtonViewSet, basename='button')

app_name = 'donation'
urlpatterns = router.urls
