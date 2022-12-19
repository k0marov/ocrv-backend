from .services import text, speech
from rest_framework import serializers

class TextSerializer(serializers.Serializer):
    id = serializers.CharField()
    text = serializers.CharField()
    note = serializers.CharField()
    completed = serializers.BooleanField()
    min_duration = serializers.IntegerField(required=False)
    max_duration = serializers.IntegerField(required=False)

class SkipDTOSerializer(serializers.Serializer):
    text_id = serializers.CharField()
    retries = serializers.IntegerField()

    def create(self, validated_data):
        return text.SkipDTO(**validated_data)

class RecordingSerializer(serializers.Serializer):
    text_id = serializers.CharField()
    speech = serializers.FileField()
    is_video = serializers.BooleanField(default=False)
    retries = serializers.IntegerField()

    def create(self, validated_data):
        return speech.Recording(**validated_data)
