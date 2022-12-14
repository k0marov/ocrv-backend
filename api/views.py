from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import renderers, status
from rest_framework.decorators import api_view
from api.services import speech_service, texts_service, api_logger

logger = api_logger.get_logger(__name__)
json_renderer = renderers.JSONRenderer()


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
    speech = request.data["speech"]
    text_id = request.data["text_id"]
    retries = request.data["retries"]
    is_video = request.data["is_video"]
    user_id = request.user.id
    speech_service.save_recording(user_id, text_id, speech, is_video)
    logger.info(f"Success text id: {text_id}; retries: {retries}")
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def skips(request: Request):
    logger.info(f'Skipped text id: {request.data["text_id"]}; retries: {request.data["retries"]}')
    return Response(status=status.HTTP_200_OK)

