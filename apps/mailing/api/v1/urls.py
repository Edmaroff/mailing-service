from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, MailingViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"clients", ClientViewSet, basename="clients")
router.register(r"mailings", MailingViewSet, basename="mailings")
router.register(r"messages", MessageViewSet, basename="messages")

urlpatterns = [
    path("", include(router.urls)),
]
