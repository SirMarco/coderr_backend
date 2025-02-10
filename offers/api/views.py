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


class OfferPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"


class OffersListView(GenericAPIView):
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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OffersDetailView(APIView):
    def get(self, request, pk):
        offer_detail = get_object_or_404(OfferDetail, pk=pk)
        serializer = OfferDetailSerializer(offer_detail, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
