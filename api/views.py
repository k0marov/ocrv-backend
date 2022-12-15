from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from . import serializers
from .services import text, speech


@api_view(['GET'])
def texts(request: Request):
    try:
        texts = text.get_texts()
        serialized = serializers.TextSerializer(texts, many=True).data
        return Response({'texts': serialized})
    except text.TextsFileNotFound:
        return Response({'detail': 'Файл с текстами не найден.'}, status=status.HTTP_404_NOT_FOUND)
    except text.NoTexts:
        return Response({'detail': 'Тексты не найдены'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def skips(request: Request):
    serializer = serializers.SkipDTOSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    skip = serializer.save(user_id=request.user.id)
    text.skip_text(skip)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def speeches(request: Request):
    print(request.data)
    serializer = serializers.RecordingSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    rec = serializer.save(user_id=request.user.id)
    speech.save_recording(rec)
    return Response(status=status.HTTP_200_OK)


