from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import renderers, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, logout

from api.serializers import UserSerializer, LoginRequestSerializer, TokenSerializer
from api import api_logger
from api.services import services

logger = api_logger.get_logger(__name__)
json_renderer = renderers.JSONRenderer()


@api_view()
@authentication_classes([TokenAuthentication])
def index():
    return "Test Backend Page"


@api_view(['GET'])
def texts(request: Request):
    try:
        texts = services.get_texts()
        return Response({'texts': texts})
    except services.TextsFileNotFound:
        return Response({'display_message': 'Файл не найден'}, status=status.HTTP_404_NOT_FOUND)
    except services.NoTexts:
        return Response({'display_message': 'Тексты не найдены'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def speeches(request: Request):
    speech = request.data["speech"]
    text_id = request.data["text_id"]
    retries = request.data["retries"]
    services.save_recording(text_id, speech)
    logger.info(f"Success text id: {text_id}; retries: {retries}")
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def skips(request: Request):
    logger.info(f'Skipped text id: {request.data["text_id"]}; retries: {request.data["retries"]}')
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request: Request):
    # серилизация данных
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # сохраняем нового пользователя
        create_user = serializer.save()
        if create_user:
            # добавление токена
            token = Token.objects.create(user=create_user)
            json = serializer.data
            json['token'] = token.key
            return Response(json, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: Request):
    # серилизация данных
    serializer = LoginRequestSerializer(data=request.data)
    if serializer.is_valid():
        authenticated_user = authenticate(**serializer.validated_data)
        if authenticated_user is not None:
            login(request, authenticated_user)
        else:
            return Response("Неверный логин или пароль!", status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def logout(request: Request):
    logout(request)
