from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from authapi.serializers import SignUpSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request: Request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    if user:
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_200_OK)
