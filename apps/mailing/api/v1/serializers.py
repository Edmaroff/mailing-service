from rest_framework import serializers

from apps.mailing.models import Client, Mailing, Message, OperatorCode, Tag


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "phone_number", "operator_code", "tag"]


class MailingSerializer(serializers.ModelSerializer):
    filter_operator_codes = serializers.PrimaryKeyRelatedField(
        queryset=OperatorCode.objects.all(), many=True, required=False
    )
    filter_tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False
    )

    class Meta:
        model = Mailing
        fields = [
            "id",
            "start_time",
            "end_time",
            "message_text",
            "filter_operator_codes",
            "filter_tags",
        ]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "created_at", "status", "mailing", "client", "error_message"]
