from rest_framework.routers import DefaultRouter

from invitations.views import InvitationViewSet

router = DefaultRouter()
router.register('', InvitationViewSet)

urlpatterns = router.urls

