from rest_framework import serializers
from .models import Order
from offers.api.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    """
    A serializer for the Order model that manages order serialization and various operational logics such as validation and order creation.
    It ensures that only authorized users can create orders and maintain data integrity throughout the order lifecycle.
    """
    offer_detail_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
            "offer_detail_id",
        ]
        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        """
        Validates the incoming data to ensure that only customers can create orders and that an 'offer_detail_id' is provided. Checks user role and existence of the specified offer detail.
        """
        request = self.context.get("request")
        user = request.user

        if not self.instance:
            if getattr(user.profile, "type", None) != "customer":
                raise serializers.ValidationError(
                    {"detail": "Nur Kunden können Bestellungen erstellen."}
                )

            offer_detail_id = data.get("offer_detail_id")
            if not offer_detail_id:
                raise serializers.ValidationError(
                    {"detail": "Offer detail ID ist notwendig."}
                )

            try:
                offer_detail = OfferDetail.objects.select_related("offer").get(
                    id=offer_detail_id
                )
                data["offer_detail"] = offer_detail
            except OfferDetail.DoesNotExist:
                 raise serializers.ValidationError(
                     {"detail": "Das Angebotsdetail existiert nicht."}
                 )

        return data

    def create(self, validated_data):
        """
        Creates a new Order instance using the validated data, including retrieving relevant offer details and setting the order's initial status to 'in progress'.
        """
        offer_detail = validated_data.pop("offer_detail")
        user = self.context["request"].user

        order = Order.objects.create(
            customer_user=user,
            business_user=offer_detail.offer.user,
            title=offer_detail.offer.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress",
        )
        return order

    def update(self, instance, validated_data):
        """
        Updates the status of an existing order. Validates that no fields other than 'status' are being updated, maintaining consistency and integrity.
        """
        if "status" in validated_data:
            instance.status = validated_data["status"]
            instance.save()
        else:
            raise serializers.ValidationError(
                {"detail": "Nur Status darf aktualisiert werden."}
            )
        return instance
