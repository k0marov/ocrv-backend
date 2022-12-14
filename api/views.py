from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import renderers, status
from rest_framework.decorators import api_view

import serializers
from api.services import speech_service, texts_service, api_logger

@api_view(['GET'])
def texts(request: Request):
    try:
        csv_texts = texts_service.get_texts()
        return Response({'texts': csv_texts})
    except texts_service.TextsFileNotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except texts_service.NoTexts:
        return Response({'detail': 'Тексты не найдены'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def speeches(request: Request):
    rec = serializers.RecordingSerializer(data=request.data).save(user_id=request.user.id)
    speech_service.save_recording(rec)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def skips(request: Request):
    skip = serializers.SkipDTOSerializer(data=request.data).save(user_id=request.user.id)
    texts_service.skip_text(skip)
    return Response(status=status.HTTP_200_OK)

