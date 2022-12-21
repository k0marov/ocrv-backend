from rest_framework import status
from rest_framework.response import Response

from api import serializers
from api.di import deps
from api.features import texts, speeches
from api.features.speeches.domain import values
from common.exceptions import error_response
from common.time import format_duration


def save_recording_with_exceptions(rec: values.Recording) -> Response:
    try:
        completed_status = deps.speeches.save_recording(rec)
        serialized = serializers.CompletedStatusSerializer(completed_status).data
        return Response(serialized)
    except texts.TextNotFound:
        return error_response(
            'Текст с указанным id не найден.',
            status.HTTP_404_NOT_FOUND
        )
    except speeches.MinDurationException as e:
        return error_response(
            f'Не соблюдено мин. время начитки.\nТребуется {format_duration(e.want)}, получено {format_duration(e.got)}.',
            status.HTTP_400_BAD_REQUEST
        )
    except speeches.MaxDurationException as e:
        return error_response(
            f'Не соблюдено макс. время начитки.\nТребуется {format_duration(e.want)}, получено {format_duration(e.got)}.',
            status.HTTP_400_BAD_REQUEST
        )
