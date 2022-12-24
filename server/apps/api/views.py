from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view

from . import serializers
from .di import deps
from .exceptions import save_recording_with_exceptions


@api_view(['GET'])
def get_texts(request: Request):
    texts = deps.texts.get_texts(str(request.user.id))
    serialized = serializers.TextSerializer(texts, many=True).data
    return Response({'texts': serialized})

@api_view(['POST'])
def skips(request: Request):
    serializer = serializers.SkipDTOSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    skip = serializer.save(user_id=request.user.id)
    deps.texts.skip_text(skip)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def post_speech(request: Request):
    serializer = serializers.RecordingSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    rec = serializer.save(by_user_id=str(request.user.id))
    return save_recording_with_exceptions(rec)



