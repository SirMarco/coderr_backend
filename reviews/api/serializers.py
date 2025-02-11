from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["reviewer", "created_at", "updated_at"]

    def validate(self, data):
        user = self.context["request"].user
        if user.profile.type != "customer":
            raise serializers.ValidationError(
                {"detail": "Nur Kunden können Bewertungen erstellen."}
            )

        business_user = data.get("business_user")
        if business_user == user:
            raise serializers.ValidationError(
                {"detail": "Sie können sich nicht selbst bewerten."}
            )

        return data

    def create(self, validated_data):
        validated_data["reviewer"] = self.context["request"].user
        return super().create(validated_data)
