from django.contrib import admin
from orders.api.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_user",
        "business_user",
        "title",
        "price",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("title", "customer_user__username", "business_user__username")
    ordering = ("-created_at",)
