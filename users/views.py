from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def authorization_api_view(request):
    # validation
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # authentication
    user = authenticate(**serializer.validated_data)

    # if user exists return key else error
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def registration_api_view(request):
    # validation
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # receive data
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    # create user
    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )

    # create code (6-symbol) -> user -> valid_until

    # return response
    return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)
