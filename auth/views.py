from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from auth.serializers import UserSerializer, LoginRequestSerializer, TokenSerializer

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
