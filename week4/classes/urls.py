from rest_framework.routers import DefaultRouter

from classes.views import ClassViewSet

router = DefaultRouter()
router.register('', ClassViewSet)

urlpatterns = router.urls
