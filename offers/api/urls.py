from django.urls import path
from .views import OffersListCreateView, OfferDetailView, OffersDetailView

urlpatterns = [
    path("offers/", OffersListCreateView.as_view(), name="offer-list-create"),
    path("offers/<int:pk>/", OfferDetailView.as_view(), name="offer-detail"),
    path("offerdetails/<int:pk>/", OffersDetailView.as_view(), name="offer-details"),
]
