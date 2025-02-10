from django.urls import path
from .views import OffersListView, OfferDetailView, OffersDetailView

urlpatterns = [
    path("offers/", OffersListView.as_view(), name="offer-list-create"),
    path("offers/<int:pk>/", OfferDetailView.as_view(), name="offer-detail"),
    path("offerdetails/<int:pk>/", OffersDetailView.as_view(), name="offer-details"),
]
