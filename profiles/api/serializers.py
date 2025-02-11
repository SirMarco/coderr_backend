from rest_framework import serializers
from profiles.api.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """
    A serializer for user profile data, linking directly to a User model and extending it with additional profile information.
    This serializer handles both the representation and update operations for UserProfile instances, ensuring data consistency and validating unique constraints like email addresses.
    """
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

    def to_representation(self, instance):
        """
        Customizes the representation of the serialized data. Modifies the file field to include a media path if the file exists.
        """
        representation = super().to_representation(instance)
        if instance.file:
            representation['file'] = f"media/{instance.file.name}" 
        else:
            representation['file'] = None
        return representation

    def update(self, instance, validated_data):
        """
        Updates the UserProfile and associated User instance based on the provided validated data. Validates email uniqueness
        outside of the current user instance.
        """
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
    """
    A serializer for business user profiles, tailored to list views that require specific fields like location, contact, and business type.
    Includes user data and customizes file representation.
    """
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
        """
        Retrieves and serializes basic user information for the associated UserProfile.
        """
        return {
            "pk": obj.user.pk,
            "username": obj.user.username,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }
    
    def to_representation(self, instance):
        """
        Modifies the default serialization to handle the media file path, ensuring it is correctly formatted or set to None if absent.
        """
        representation = super().to_representation(instance)
        if instance.file:
            representation['file'] = f"media/{instance.file.name}" 
        else:
            representation['file'] = None
        return representation


class UserProfileCustomerListSerializer(serializers.ModelSerializer):
    """
    A serializer for customer user profiles focusing on providing user identification and uploaded file details,
    used primarily for listing and retrieving customer-specific data.
    """
    user = serializers.SerializerMethodField()
    file = serializers.ImageField(required=False, allow_null=True)
    uploaded_at = serializers.DateTimeField(source="user.date_joined", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user", "file", "uploaded_at", "type"]

    def to_representation(self, instance):
            representation = super().to_representation(instance)
            if instance.file:
                representation['file'] = f"media/{instance.file.name}" 
            else:
                representation['file'] = None
            return representation
    
    def get_user(self, obj):
        """
        Serializes basic user data such as username and names, tailored for customer visibility in listings.
        """        
        return {
            "pk": obj.user.pk,
            "username": obj.user.username,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }
