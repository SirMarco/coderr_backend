from rest_framework import serializers
from profiles.api.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.pk", read_only=True)
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    file = serializers.ImageField(required=False, allow_null=True)
    created_at = serializers.CharField(source="user.date_joined")

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "email",
            "type",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "created_at",
        ]

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if instance.file:
    #         representation["file"] = instance.file.url
    #     else:
    #         representation["file"] = None
    #     return representation

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        new_email = user_data.get("email")

        if new_email and new_email != instance.user.email:
            if (
                User.objects.filter(email=new_email)
                .exclude(pk=instance.user.pk)
                .exists()
            ):
                raise serializers.ValidationError(
                    {"email": ["Diese E-Mail wird bereits verwendet."]}
                )

        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class UserProfileBusinessListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    file = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]

    def get_user(self, obj):
        return {
            "pk": obj.user.pk,
            "username": obj.user.username,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }


class UserProfileCustomerListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    file = serializers.ImageField(required=False, allow_null=True)
    uploaded_at = serializers.DateTimeField(source="user.date_joined", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user", "file", "uploaded_at", "type"]

    def get_user(self, obj):
        return {
            "pk": obj.user.pk,
            "username": obj.user.username,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }
