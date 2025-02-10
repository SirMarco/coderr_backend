from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offer")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offers_images/", blank=True, null=True)
    description = models.TextField(max_length=800, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=5, decimal_places=2)
    min_delivery_time = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.id} - {self.title}"


class OfferDetail(models.Model):
    OFFER_TYPES = [
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]

    offer = models.ForeignKey(Offer, related_name="details", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    revisions = models.IntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    features = JSONField()
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)

    def __str__(self):
        return f"{self.offer.title} - {self.offer_type}"
