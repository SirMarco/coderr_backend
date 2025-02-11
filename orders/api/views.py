from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Order, User
from .serializers import OrderSerializer
from django.db.models import Q
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from user_auth_app.permissions import OrderPermission
from user_auth_app.permissions import IsCustomerUser


class OrderListCreateView(APIView):
    """
    Allows authenticated users to list their orders and create new ones.
    - `GET`: Lists all of the user's orders, sorted by creation date in descending order.
    - `POST`: Enables the creation of a new order.
    """
   
    permission_classes = [IsCustomerUser]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).order_by("-created_at")

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Allows authenticated users and specifically authorized users to edit or delete orders.
    - `GET`: Retrieves details of a specific order.
    - `PATCH`: Updates an order if the user is authorized.
    - `DELETE`: Deletes an order if the user is authorized.
    """  
    permission_classes = [OrderPermission]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def patch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs["pk"])
        user = request.user

        if getattr(user.profile, "type", None) != "business":
            return Response(
                {"detail": "Nur Anbieter können Bestellungen ändern."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(
            order, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid():
            updated_order = serializer.save()
            return Response(
                OrderSerializer(updated_order, context={"request": request}).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs["pk"])
        user = request.user

        if not user.is_staff and order.customer_user != user:
            return Response(
                {"detail": "Nur Admins oder der Kunde können eine Bestellung löschen."},
                status=status.HTTP_403_FORBIDDEN,
            )

        order.delete()
        return Response(
            {"detail": "Bestellung erfolgreich gelöscht."}, status=status.HTTP_200_OK
        )


class OrderCountView(APIView):
    """
    Returns the number of orders in progress for a specific business user.
    - `GET`: Counts the orders in progress for a business user.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        business_user_id = kwargs.get("pk")

        business_user = User.objects.filter(pk=business_user_id).first()
        if not business_user:
            return Response(
                {"detail": "Business user not found."}, status=status.HTTP_404_NOT_FOUND
            )

        orders = Order.objects.filter(business_user=business_user, status="in_progress")
        order_count = orders.count()
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """
    Returns the number of completed orders for a specific business user.
    - `GET`: Counts the completed orders for a business user.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        business_user_id = kwargs.get("pk")

        business_user = User.objects.filter(pk=business_user_id).first()
        if not business_user:
            return Response(
                {"detail": "Business user not found."}, status=status.HTTP_404_NOT_FOUND
            )

        orders = Order.objects.filter(business_user=business_user, status="completed")
        order_count = orders.count()
        return Response(
            {"completed_order_count": order_count}, status=status.HTTP_200_OK
        )
