from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from rest_framework import renderers, status
from rest_framework.decorators import api_view
from api import api_logger
import os
import csv

from api.services import services

logger = api_logger.get_logger(__name__)
json_renderer = renderers.JSONRenderer()


@api_view(['GET'])
def index(request):
    return Response('Test backend page')


@api_view(['GET'])
def texts(request):
    try:
        texts = services.get_texts()
        return Response({'texts': texts})
    except services.TextsFileNotFound:
        return Response({'display_message': 'Файл не найден'}, status=status.HTTP_404_NOT_FOUND)
    except services.NoTexts:
        return Response({'display_message': 'Тексты не найдены'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def speeches(request):
    speech = request.data["speech"]
    text_id = request.data["text_id"]
    retries = request.data["retries"]
    services.save_recording(text_id, speech)
    logger.info(f"Success text id: {text_id}; retries: {retries}")
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def skips(request):
    logger.info(f'Skipped text id: {request.data["text_id"]}; retries: {request.data["retries"]}')
    return Response(status=status.HTTP_200_OK)
