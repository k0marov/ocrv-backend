from rest_framework import serializers

from .features.filepaths.domain.values import RecordingMeta
from .features.texts.domain.values import SkipDTO
from .features.speeches.domain.values import Recording

class CompletedStatusSerializer(serializers.Serializer):
    url = serializers.CharField()
    is_video = serializers.BooleanField()

class TextSerializer(serializers.Serializer):
    id = serializers.CharField(source='model.id')
    text = serializers.CharField(source='model.text')
    note = serializers.CharField(source='model.note')
    completed = CompletedStatusSerializer(required=False)
    min_duration = serializers.IntegerField(source='model.min_duration', required=False)
    max_duration = serializers.IntegerField(source='model.max_duration', required=False)


class SkipDTOSerializer(serializers.Serializer):
    text_id = serializers.CharField()
    retries = serializers.IntegerField()

    def create(self, validated_data):
        return SkipDTO(**validated_data)

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
        return Recording(
            meta=RecordingMeta(
                text_id=validated_data.get('text_id'),
                is_video=validated_data.get('is_video'),
                by_user_id=validated_data.get('by_user_id'),
            ),
            retries=validated_data.get('retries'),
            tmp_blob_path=validated_data.get('speech').temporary_file_path(),
        )
