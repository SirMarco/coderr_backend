from django.urls import path
from .views import (
    OrderListCreateView,
    OrderRetrieveUpdateDestroyView,
    OrderCountView,
    CompletedOrderCountView,
)

urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="order-create"),
    path(
        "orders/<int:pk>/",
        OrderRetrieveUpdateDestroyView.as_view(),
        name="orders-detail",
    ),
    path("order-count/<int:pk>/", OrderCountView.as_view(), name="order-count"),
    path(
        "completed-order-count/<int:pk>/",
        CompletedOrderCountView.as_view(),
        name="completed-order-count",
    ),
]
