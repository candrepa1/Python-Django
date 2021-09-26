from rest_framework.routers import DefaultRouter

from teachers.views import TeacherViewSet

router = DefaultRouter()
router.register('', TeacherViewSet)

urlpatterns = router.urls
