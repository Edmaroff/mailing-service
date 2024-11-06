from django.contrib import admin

from .models import Client, Mailing, Message, OperatorCode, Tag


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time", "message_text")
    list_filter = ("start_time", "end_time")
    search_fields = ("message_text",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "operator_code", "tag")
    list_filter = ("operator_code", "tag")
    search_fields = ("phone_number",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "status", "mailing", "client")
    list_filter = ("status", "mailing", "client")
    search_fields = ("client__phone_number",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(OperatorCode)
class OperatorCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "code")
    search_fields = ("code",)
