from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework import status


class ReviewListCreateView(ListCreateAPIView):
    """
    API-Endpoint zur Auflistung aller Bewertungen oder zur Erstellung neuer Bewertungen.
    - `GET`: Listet alle Bewertungen auf. Unterstützt Filterung nach `business_user_id` und `reviewer_id`.
    - `POST`: Ermöglicht Kunden das Erstellen neuer Bewertungen.
    Die Erstellung ist auf Nutzer beschränkt, die als 'customer' im Profil typisiert sind.
    """    
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
    """
    API-Endpoint für den Zugriff auf spezifische Bewertungen und deren Bearbeitung oder Löschung.
    - `GET`: Ruft eine spezifische Bewertung ab.
    - `PATCH`: Erlaubt die Aktualisierung einer Bewertung, sofern der Nutzer der ursprüngliche Verfasser oder ein Admin ist.
    - `DELETE`: Erlaubt das Löschen einer Bewertung unter denselben Bedingungen.
    Zugriff ist auf authentifizierte Nutzer beschränkt.
    """    
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
