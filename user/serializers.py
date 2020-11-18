from django.contrib.auth import authenticate
from passlib.hash import pbkdf2_sha256
from rest_framework import serializers

from user import models


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Phone
        fields = ('number', 'area_code', 'country_code')


class UserSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True)
    last_login = serializers.DateTimeField(read_only=True, format="%d/%m/%Y")
    created_at = serializers.DateTimeField(read_only=True, format="%d/%m/%Y")

    class Meta:
        model = models.User
        fields = (
            'first_name', 'last_name', 'email', 'password', 'phones',
            'last_login', 'created_at')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        phones = validated_data.pop('phones')
        validated_data['password'] = pbkdf2_sha256.encrypt(
            validated_data.pop('password'), rounds=12000, salt_size=32
        )
        user = models.User.objects.create(**validated_data)

        for phone_data in phones:
            models.Phone.objects.create(user=user, **phone_data)
        return user


class SigninSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = models.User.objects.filter(email=data['email'])

        if user:
            user = user.first()
            password = data['password']
            if user.verify_password(password) and user.is_active:
                return user
        raise serializers.ValidationError("Credenciais inválidas.")
