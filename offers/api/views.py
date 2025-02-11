from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer
from rest_framework.pagination import PageNumberPagination
from user_auth_app.permissions import IsBusinessUser


class OfferPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"


class OffersListCreateView(GenericAPIView):
    """
    Lists offers and allows for the creation of new offers.
    Supports filtering, sorting, and searching within the offers.
    Uses the `OfferPagination` class for paginating the results.
    """

    permission_classes = [IsBusinessUser]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = OfferPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = {
        "user_id": ["exact"],
        "min_price": ["gte"],
        "min_delivery_time": ["lte"],
    }

    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price", "min_delivery_time"]

    def get_queryset(self):
        queryset = super().get_queryset()

        creator_id = self.request.query_params.get("creator_id")
        if creator_id:
            queryset = queryset.filter(user_id=creator_id)

        max_delivery_time = self.request.query_params.get("max_delivery_time")
        if max_delivery_time:
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time)

        return queryset

    def get(self, request):
        offers = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(offers)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy() 
        details = data.get("details", [])
        if details:
            data["min_price"] = min(detail["price"] for detail in details)
            data["min_delivery_time"] = min(detail["delivery_time_in_days"] for detail in details)

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferDetailView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a single offer.
    Uses the `OfferSerializer` for serializing the offer data.
    """

    permission_classes = [IsBusinessUser]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OffersDetailView(APIView):
    """
    API endpoint for retrieving the detailed information of a specific offer.
    Fetches the corresponding offer using the `get_object_or_404` method to ensure it exists.
    """

    def get(self, request, pk):
        offer_detail = get_object_or_404(OfferDetail, pk=pk)
        serializer = OfferDetailSerializer(offer_detail, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
