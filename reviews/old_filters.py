from django_filters import rest_framework as filters
from .models import Review


class ReviewFilter(filters.FilterSet):
    business_user_id = filters.NumberFilter(field_name="business_user_id")
    reviewer_id = filters.NumberFilter(field_name="reviewer_id")
    ordering = filters.OrderingFilter(fields=["updated_at", "rating"])

    class Meta:
        model = Review
        fields = ["business_user_id", "reviewer_id"]
