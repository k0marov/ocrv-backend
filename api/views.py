from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view

from common.exceptions import error_response
from common.time import format_duration
from . import serializers
from .services import text, speech


@api_view(['GET'])
def texts(request: Request):
    texts = text.get_texts()
    serialized = serializers.TextSerializer(texts, many=True).data
    return Response({'texts': serialized})

@api_view(['POST'])
def skips(request: Request):
    serializer = serializers.SkipDTOSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    skip = serializer.save(user_id=request.user.id)
    text.skip_text(skip)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def speeches(request: Request):
    serializer = serializers.RecordingSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    rec = serializer.save(user_id=request.user.id)
    # TODO: factor out the error handling
    try:
        speech.save_recording(rec)
    except text.TextNotFound:
        return error_response(
            'Текст с указанным id не найден.',
            status.HTTP_404_NOT_FOUND
        )
    except speech.MinDurationException as e:
        return error_response(
            f'Не соблюдено мин. время начитки.\nТребуется {format_duration(e.want)}, получено {format_duration(e.got)}.',
            status.HTTP_400_BAD_REQUEST
        )
    except speech.MaxDurationException as e:
        return error_response(
            f'Не соблюдено макс. время начитки.\nТребуется {format_duration(e.want)}, получено {format_duration(e.got)}.',
            status.HTTP_400_BAD_REQUEST
        )


    return Response(status=status.HTTP_200_OK)


