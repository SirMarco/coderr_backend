from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from reviews.api.models import Review
from django.db.models import Avg
from offers.api.models import Offer
from django.contrib.auth.models import User


class BaseInfoView(APIView):
    """
    Handles GET requests to retrieve counts and averages from different models.
    Returns the total number of reviews, the average rating of reviews, the count of user profiles marked as 'business', 
    and the total number of offers. All values are returned in a JSON response.
    """ 
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(Avg("rating"))["rating__avg"] or 0
        business_profile_count = User.objects.filter(profile__type="business").count()
        offer_count = Offer.objects.count()

        return Response(
            {
                "review_count": review_count,
                "average_rating": round(average_rating, 1),
                "business_profile_count": business_profile_count,
                "offer_count": offer_count,
            }
        )
