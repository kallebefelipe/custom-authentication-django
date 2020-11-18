from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.models import User

from user import serializers


class SignupView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = RefreshToken.for_user(user)
        data = {
            'token': str(token.access_token)
        }

        return Response(
            data, status=status.HTTP_201_CREATED
        )


class SigninView(generics.GenericAPIView):
    serializer_class = serializers.SigninSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token = RefreshToken.for_user(user)

        return Response({
            'user': serializers.UserSerializer(
                user, context=self.get_serializer_context()).data,
            'token': str(token.access_token)
        })


class MeView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
