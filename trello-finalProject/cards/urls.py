from rest_framework.routers import DefaultRouter

from cards.views import CardViewSet

router = DefaultRouter()
router.register('', CardViewSet)

urlpatterns = router.urls


