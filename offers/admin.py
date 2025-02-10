from django.contrib import admin
from .api.models import Offer, OfferDetail


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "updated_at")
    list_filter = ("user", "created_at", "updated_at")
    search_fields = ("title", "description")


class OfferDetailAdmin(admin.ModelAdmin):
    list_display = (
        "offer",
        "revisions",
        "delivery_time_in_days",
        "price",
        "offer_type",
    )
    list_filter = ("offer", "offer_type")
    search_fields = ("offer__title", "offer__description")


admin.site.register(OfferDetail, OfferDetailAdmin)
