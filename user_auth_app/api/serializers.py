from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.api.models import UserProfile
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": ["Dieser Benutzername existiert nicht."]}
            )

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                {"password": ["Das Passwort ist falsch."]}
            )

        data["user"] = user
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": ["Dieser Benutzername ist bereits vergeben."]}
            )
        return value

    def validate(self, data):
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError(
                {"password": ["Die Passwörter stimmen nicht überein."]}
            )
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": ["Diese E-Mail wird bereits verwendet."]}
            )
        return data

    def save(self, request):
        user = User(
            username=self.validated_data["username"], email=self.validated_data["email"]
        )
        user.set_password(self.validated_data["password"])
        user.save()

        UserProfile.objects.create(user=user, type=self.validated_data["type"])
        return user
