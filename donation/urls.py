from rest_framework.routers import SimpleRouter

from .views import ButtonsViewSet, DonationsViewSet, SectionsViewSet

router = SimpleRouter(use_regex_path=False)  # type: ignore [call-arg]  # use_regex_path param exists
router.register('donations', DonationsViewSet, basename='donation')
router.register('sections', SectionsViewSet, basename='section')
router.register('buttons', ButtonsViewSet, basename='button')

app_name = 'donation'
urlpatterns = router.urls
