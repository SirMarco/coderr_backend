from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from profiles.api.models import UserProfile
from .serializers import (
    UserProfileSerializer,
    UserProfileCustomerListSerializer,
    UserProfileBusinessListSerializer,
)
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


class UserProfileList(ListCreateAPIView):
    """
    API-Endpoint zur Auflistung aller Benutzerprofile oder zur Erstellung eines neuen Profils.
    - `GET`: Listet alle Benutzerprofile auf.
    - `POST`: Ermöglicht das Erstellen eines neuen Benutzerprofils.
    Verwendet `UserProfileSerializer` zur Serialisierung der Daten.
    """    
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(RetrieveUpdateDestroyAPIView):
    """
    API-Endpoint für den Zugriff auf ein spezifisches Benutzerprofil und dessen Bearbeitung oder Löschung.
    - `GET`: Ruft ein spezifisches Benutzerprofil ab.
    - `PATCH`: Aktualisiert ein Benutzerprofil, wenn der authentifizierte Nutzer der Besitzer ist.
    - `DELETE`: Löscht ein Benutzerprofil, wenn der authentifizierte Nutzer der Besitzer ist.
    Nur authentifizierte Nutzer haben Zugriff auf diese Methoden.
    """    
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        user_id = self.kwargs.get("pk")

        profile = get_object_or_404(UserProfile, user_id=user_id)

        if self.request.method in ["PATCH"] and profile.user != user:
            raise PermissionDenied(
                "Du darfst nur dein eigenes Profil bearbeiten oder löschen."
            )

        return profile


class BusinessProfileList(ListAPIView):
    """
    API-Endpoint zur Auflistung aller Geschäftsprofile.
    - `GET`: Listet alle Profile auf, die als 'business' typisiert sind.
    Verwendet `UserProfileBusinessListSerializer` zur spezifischen Serialisierung von Geschäftsprofilen.
    """    
    queryset = UserProfile.objects.filter(type="business")
    serializer_class = UserProfileBusinessListSerializer


class CustomerProfileList(ListAPIView):
    """
    API-Endpoint zur Auflistung aller Kundenprofile.
    - `GET`: Listet alle Profile auf, die als 'customer' typisiert sind.
    Verwendet `UserProfileCustomerListSerializer` zur spezifischen Serialisierung von Kundenprofilen.
    """    
    queryset = UserProfile.objects.filter(type="customer")
    serializer_class = UserProfileCustomerListSerializer
