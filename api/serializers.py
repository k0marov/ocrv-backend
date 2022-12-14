from api.services import texts_service
from services import speech_service
from rest_framework import serializers

class TextSerializer(serializers.Serializer):
    id = serializers.CharField()
    text = serializers.CharField()
    note = serializers.CharField()
    min_duration = serializers.IntegerField(required=False)
    max_duration = serializers.IntegerField(required=False)

class SkipDTOSerializer(serializers.Serializer):
    text_id = serializers.CharField()
    retries = serializers.IntegerField()

    def create(self, validated_data):
        return texts_service.SkipDTO(
            user_id=validated_data.get('user_id'),
            text_id=validated_data.get('text_id'),
            retries=validated_data.get('retries'),
        )

class RecordingSerializer(serializers.Serializer):
    text_id = serializers.CharField()
    speech = serializers.FileField()
    is_video = serializers.BooleanField(default=False)
    retries = serializers.IntegerField()

    def create(self, validated_data):
        return speech_service.Recording(
            text_id=validated_data.get('text_id'),
            speech=validated_data.get('speech'),
            is_video=validated_data.get('is_video'),
            retries=validated_data.get('retries'),
            user_id=validated_data.get('user_id'),
        )
