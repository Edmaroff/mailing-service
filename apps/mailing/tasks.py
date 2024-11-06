from celery import shared_task
from django.utils import timezone

from .models import Mailing
from .utils import send_messages_for_mailing


@shared_task
def send_mailing_task(mailing_id):
    try:
        mailing = Mailing.objects.get(id=mailing_id)
        current_time = timezone.now()

        # Проверяем, что время начала рассылки наступило и не превысило время окончания
        if mailing.start_time <= current_time <= mailing.end_time:
            send_messages_for_mailing(mailing)

    except Mailing.DoesNotExist:
        print(f"Рассылка {mailing_id} не существует")
