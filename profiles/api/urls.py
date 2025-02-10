from django.urls import path
from .views import (
    UserProfileList,
    UserProfileDetail,
    CustomerProfileList,
    BusinessProfileList,
)

urlpatterns = [
    path("profile/", UserProfileList.as_view(), name="userprofile-list"),
    path("profile/<int:pk>/", UserProfileDetail.as_view(), name="userprofile-detail"),
    path(
        "profiles/customer/",
        CustomerProfileList.as_view(),
        name="customer-profiles-list",
    ),
    path(
        "profiles/business/",
        BusinessProfileList.as_view(),
        name="business-profiles-list",
    ),
]
