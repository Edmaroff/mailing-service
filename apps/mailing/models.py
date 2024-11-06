import re

from django.core.exceptions import ValidationError
from django.db import models

MESSAGE_STATUS_PENDING = "pending"
MESSAGE_STATUS_SENT = "sent"
MESSAGE_STATUS_FAILED = "failed"

MESSAGE_STATUS_CHOICES = [
    (MESSAGE_STATUS_PENDING, "Ожидание"),
    (MESSAGE_STATUS_SENT, "Отправлено"),
    (MESSAGE_STATUS_FAILED, "Не удалось"),
]


def validate_phone_number(value):
    pattern = r"^7\d{10}$"
    if not re.match(pattern, value):
        raise ValidationError(
            "Номер телефона должен быть в формате 7XXXXXXXXXX, где X - цифра от 0 до 9)"
        )


def validate_operator_code(value):
    pattern = r"^\d{3}$"
    if not re.match(pattern, value):
        raise ValidationError("Код оператора должен состоять из 3 цифр")


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Тег")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class OperatorCode(models.Model):
    code = models.CharField(
        max_length=3,
        unique=True,
        verbose_name="Код оператора",
        validators=[validate_operator_code],
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Код оператора"
        verbose_name_plural = "Коды операторов"


class Client(models.Model):
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="Номер телефона",
        validators=[validate_phone_number],
    )
    operator_code = models.ForeignKey(
        OperatorCode,
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name="Код оператора",
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="clients", verbose_name="Тег"
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        indexes = [
            models.Index(fields=["operator_code", "tag"], name="operator_tag_idx")
        ]

    def __str__(self):
        return f"Клиент {self.id} - {self.phone_number}"


class Mailing(models.Model):
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время окончания")
    message_text = models.TextField(verbose_name="Текст сообщения")

    filter_operator_codes = models.ManyToManyField(
        OperatorCode,
        blank=True,
        related_name="mailings",
        verbose_name="Фильтр по кодам операторов",
    )
    filter_tags = models.ManyToManyField(
        Tag, blank=True, related_name="mailings", verbose_name="Фильтр по тегам"
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F("start_time")),
                name="check_end_time_gt_start_time",
            )
        ]

    def __str__(self):
        return f"Рассылка {self.id}. Начало: {self.start_time}, конец: {self.end_time}"


class Message(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Дата и время отправки", auto_now_add=True
    )
    status = models.CharField(
        max_length=20,
        choices=MESSAGE_STATUS_CHOICES,
        default="pending",
        verbose_name="Статус",
    )

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Рассылка",
    )
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="messages", verbose_name="Клиент"
    )
    error_message = models.TextField(
        null=True, blank=True, verbose_name="Сообщение об ошибке"
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"Сообщение {self.id} в рассылке {self.mailing}"
