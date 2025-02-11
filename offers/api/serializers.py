from rest_framework import serializers
from django.contrib.auth.models import User
from offers.api.models import Offer, OfferDetail


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    A serializer for the OfferDetail model, which serializes details of an offer including attributes like title,
    revisions, delivery time, price, and features. It provides custom validation for revisions and features
    to ensure data integrity and also includes a method to generate a URL for each OfferDetail instance.
    """
    
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "url",
        ]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"

    def validate_revisions(self, value):
        if value < -1:
            raise serializers.ValidationError(
                {"detail": "Revisionen müssen -1 oder eine positive ganze Zahl sein."}
            )
        return value

    def validate_features(self, value):
        if not value or not isinstance(value, list):
            raise serializers.ValidationError(
                {"detail": "Es sollte mindestens ein Feature vorhanden sein."}
            )
        return value


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializes the Offer model, incorporating detailed nested serialization for both offer details and user details. 
    It manages complex data interactions including custom method fields for user information and validation logic to ensure
    the integrity of offer types during creation. Additionally, this serializer handles the creation and updating of Offer instances 
    along with their related OfferDetail instances, ensuring data consistency and enforcing business rules during POST requests.
    """
    details = OfferDetailSerializer(many=True, required=False)
    user_details = UserDetailSerializer(source="user", read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_user(self, obj):
        """
        Returns the user ID associated with the offer.
        """
        return obj.user.id  

    def validate_details(self, value):
        """
        Validates that the details for a new offer include all necessary offer types ('basic', 'standard', 'premium').
        Raises a ValidationError if any required offer type is missing.
        """
        request = self.context.get("request")

        if request and request.method == "POST":
            offer_types = {detail["offer_type"] for detail in value}
            if offer_types != {"basic", "standard", "premium"}:
                raise serializers.ValidationError(
                    {"detail": "Nur: basic, standard, premium zulässig"}
                )
        return value

    def create(self, validated_data):
        """
        Creates a new Offer instance along with its associated OfferDetail instances from provided validated data.
        """
        user = validated_data.pop("user", None)
        details_data = validated_data.pop("details", [])

        offer = Offer.objects.create(user=user, **validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer


    def update(self, instance, validated_data):
        """
        Updates an existing Offer instance and its associated OfferDetail instances from provided validated data.
        """
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")
                detail_instance = instance.details.filter(offer_type=offer_type).first()

                if detail_instance:
                    for attr, value in detail_data.items():
                        setattr(detail_instance, attr, value)
                    detail_instance.save()

        return instance
