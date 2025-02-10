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
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(RetrieveUpdateDestroyAPIView):
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
    queryset = UserProfile.objects.filter(type="business")
    serializer_class = UserProfileBusinessListSerializer


class CustomerProfileList(ListAPIView):
    queryset = UserProfile.objects.filter(type="customer")
    serializer_class = UserProfileCustomerListSerializer
