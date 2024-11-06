from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.mailing.models import Client, Mailing, Message
from apps.mailing.tasks import send_mailing_task

from .serializers import ClientSerializer, MailingSerializer, MessageSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mailing = serializer.save()

        # Проверяем время начала рассылки и отправляем задачу в Celery
        current_time = timezone.now()
        if mailing.start_time <= current_time <= mailing.end_time:
            # Запускаем рассылку сразу
            send_mailing_task.delay(mailing.id)
        elif mailing.start_time > current_time:
            # Отложенный запуск рассылки
            delay = (mailing.start_time - current_time).total_seconds()
            send_mailing_task.apply_async((mailing.id,), countdown=delay)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
