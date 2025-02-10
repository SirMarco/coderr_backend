from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework import status


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["business_user_id", "reviewer_id"]
    ordering = ["updated_at", "rating"]

    def perform_create(self, serializer):
        user = self.request.user
        if user.profile.type != "customer":
            raise PermissionDenied(
                {"error": "Nur Kunden können Bewertungen erstellen."}
            )
        serializer.save(reviewer=user)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_object(self):
        review = super().get_object()
        user = self.request.user

        if (
            self.request.method in ["PATCH", "DELETE"]
            and review.reviewer != user
            and not user.is_staff
        ):
            raise PermissionDenied(
                {
                    "error": "Sie können nur Ihre eigenen Bewertungen bearbeiten oder löschen."
                }
            )

        return review

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
