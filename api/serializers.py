from .features import text, speech
from rest_framework import serializers

from .features.filepaths.domain.values import RecordingMeta


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
    """
    by_user_id must be passed in as a context argument when deserializing

    The speech file must always be a TemporaryUploadedFile and NOT InMemoryUploadedFile.
    This can be ensured by setting FILE_UPLOAD_MAX_MEMORY_SIZE to 0
    """
    text_id = serializers.CharField()
    speech = serializers.FileField()
    is_video = serializers.BooleanField(default=False)
    retries = serializers.IntegerField()

    def create(self, validated_data):
        return speech.Recording(
            meta=RecordingMeta(
                text_id=validated_data.get('text_id'),
                is_video=validated_data.get('is_video'),
                by_user_id=validated_data.get('by_user_id'),
            ),
            retries=validated_data.get('retries'),
            tmp_blob_path=validated_data.get('speech').temporary_file_path(),
        )
