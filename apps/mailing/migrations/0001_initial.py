# Generated by Django 5.1.2 on 2024-11-06 12:53

import apps.mailing.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        max_length=11,
                        unique=True,
                        validators=[apps.mailing.models.validate_phone_number],
                        verbose_name="Номер телефона",
                    ),
                ),
            ],
            options={
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
            },
        ),
        migrations.CreateModel(
            name="Mailing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField(verbose_name="Время начала")),
                ("end_time", models.DateTimeField(verbose_name="Время окончания")),
                ("message_text", models.TextField(verbose_name="Текст сообщения")),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
        migrations.CreateModel(
            name="OperatorCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=3,
                        unique=True,
                        validators=[apps.mailing.models.validate_operator_code],
                        verbose_name="Код оператора",
                    ),
                ),
            ],
            options={
                "verbose_name": "Код оператора",
                "verbose_name_plural": "Коды операторов",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=50, unique=True, verbose_name="Тег"),
                ),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата и время отправки"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Ожидание"),
                            ("sent", "Отправлено"),
                            ("failed", "Не удалось"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "error_message",
                    models.TextField(
                        blank=True, null=True, verbose_name="Сообщение об ошибке"
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="mailing.client",
                        verbose_name="Клиент",
                    ),
                ),
                (
                    "mailing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="mailing.mailing",
                        verbose_name="Рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
            },
        ),
        migrations.AddField(
            model_name="mailing",
            name="filter_operator_codes",
            field=models.ManyToManyField(
                blank=True,
                related_name="mailings",
                to="mailing.operatorcode",
                verbose_name="Фильтр по кодам операторов",
            ),
        ),
        migrations.AddField(
            model_name="client",
            name="operator_code",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="clients",
                to="mailing.operatorcode",
                verbose_name="Код оператора",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="filter_tags",
            field=models.ManyToManyField(
                blank=True,
                related_name="mailings",
                to="mailing.tag",
                verbose_name="Фильтр по тегам",
            ),
        ),
        migrations.AddField(
            model_name="client",
            name="tag",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="clients",
                to="mailing.tag",
                verbose_name="Тег",
            ),
        ),
        migrations.AddConstraint(
            model_name="mailing",
            constraint=models.CheckConstraint(
                condition=models.Q(("end_time__gt", models.F("start_time"))),
                name="check_end_time_gt_start_time",
            ),
        ),
        migrations.AddIndex(
            model_name="client",
            index=models.Index(
                fields=["operator_code", "tag"], name="operator_tag_idx"
            ),
        ),
    ]
