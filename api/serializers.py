from services import speech_service
from rest_framework import serializers
class RecordingSerializer(serializers.Serializer):
    text_id = serializers.CharField(max_length=50)
    speech = serializers.FileField()
    is_video = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return speech_service.Recording(
            text_id=validated_data.get('text_id'),
            speech=validated_data.get('speech'),
            is_video=validated_data.get('is_video'),
            retries=validated_data.get('retries'),
            user_id=validated_data.get('user_id'),
        )