from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import renderers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from api.serializers import UserSerializer, LoginRequestSerializer, TokenSerializer
from api.services import services, api_logger

logger = api_logger.get_logger(__name__)
json_renderer = renderers.JSONRenderer()


@api_view(['GET'])
def texts(request: Request):
    try:
        csv_texts = services.get_texts()
        return Response({'texts': csv_texts})
    except services.TextsFileNotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except services.NoTexts:
        return Response({'detail': 'Тексты не найдены'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def speeches(request: Request):
    speech = request.data["speech"]
    text_id = request.data["text_id"]
    retries = request.data["retries"]
    user_id = request.user.id
    services.save_recording(user_id, text_id, speech)
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
def login(request):
    # серилизация данных
    serializer = LoginRequestSerializer(data=request.data)
    if serializer.is_valid():
        authenticated_user = authenticate(**serializer.validated_data)
        if authenticated_user is None:
            return Response("Неверный логин или пароль!", status=status.HTTP_400_BAD_REQUEST)
        # создание токена
        token = Token.objects.create(user=authenticated_user)
        return Response(TokenSerializer(token).data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def logout(request):
    current_user = UserSerializer(request.user)
    Token.objects.filter(user=current_user).delete()
    return Response(status=status.HTTP_200_OK)
