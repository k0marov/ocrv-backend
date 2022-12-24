from rest_framework import status
from rest_framework.response import Response

from apps.api import serializers
from apps.api.di import deps
from apps.api.features import speeches
from apps.api.features import texts
from apps.api.features.speeches.domain import values
from apps.common.exceptions import error_response
from apps.common.time import format_duration


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
