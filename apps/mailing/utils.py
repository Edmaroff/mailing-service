from django.db.models import Q
from django.utils import timezone

from .models import (
    MESSAGE_STATUS_FAILED,
    MESSAGE_STATUS_PENDING,
    MESSAGE_STATUS_SENT,
    Client,
    Message,
)


def send_messages_for_mailing(mailing):
    """Отправляет сообщения всем клиентам, подходящим под фильтры рассылки."""
    # Фильтруем клиентов по кодам и тегам, указанным в рассылке
    client_filter = Q()

    # Фильтры по коду оператора
    if mailing.filter_operator_codes.exists():
        client_filter &= Q(operator_code__in=mailing.filter_operator_codes.all())

    # Фильтры по тегу
    if mailing.filter_tags.exists():
        client_filter &= Q(tag__in=mailing.filter_tags.all())

    clients = Client.objects.filter(client_filter).distinct()

    for client in clients:
        # Проверяем время окончания рассылки перед отправкой каждого сообщения
        if timezone.now() > mailing.end_time:
            print(
                "Время окончания рассылки прошло, оставшиеся сообщения не будут отправлены."
            )
            break

        message = Message.objects.create(
            mailing=mailing,
            client=client,
            status=MESSAGE_STATUS_PENDING,
        )

        # Симуляция отправки сообщения, через стороннее API
        try:
            print(f"Отправка сообщения {client.phone_number}: {mailing.message_text}")
            message.status = MESSAGE_STATUS_SENT
            message.save()
        except Exception as e:
            error_msg = str(e)
            message.status = MESSAGE_STATUS_FAILED
            message.error_message = error_msg
            message.save()
