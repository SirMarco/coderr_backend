from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Order, User
from .serializers import OrderSerializer
from django.db.models import Q
from rest_framework.generics import RetrieveUpdateDestroyAPIView


class OrderListCreateView(APIView):
    """
    Erlaubt es authentifizierten Nutzern, ihre Bestellungen aufzulisten und neue Bestellungen zu erstellen.
    - `GET`: Listet alle Bestellungen des Nutzers, sortiert nach Erstellungsdatum absteigend.
    - `POST`: Ermöglicht das Erstellen einer neuen Bestellung.
    """    
    permission_classes = [IsAuthenticated]

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
    Erlaubt es authentifizierten Nutzern und spezifisch berechtigten Nutzern, Bestellungen zu bearbeiten oder zu löschen.
    - `GET`: Ruft Details einer spezifischen Bestellung ab.
    - `PATCH`: Aktualisiert eine Bestellung, wenn der Nutzer berechtigt ist.
    - `DELETE`: Löscht eine Bestellung, wenn der Nutzer berechtigt ist.
    """    
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def patch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs["pk"])
        user = request.user

        if getattr(user.profile, "type", None) != "business":
            return Response(
                {"error": "Nur Anbieter können Bestellungen ändern."},
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
                {"error": "Nur Admins oder der Kunde können eine Bestellung löschen."},
                status=status.HTTP_403_FORBIDDEN,
            )

        order.delete()
        return Response(
            {"message": "Bestellung erfolgreich gelöscht."}, status=status.HTTP_200_OK
        )


class OrderCountView(APIView):
    """
    Gibt die Anzahl der in Bearbeitung befindlichen Bestellungen eines spezifischen Geschäftsnutzers zurück.
    - `GET`: Zählt die in Bearbeitung befindlichen Bestellungen eines Geschäftsnutzers.
    """    
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        business_user_id = kwargs.get("pk")

        business_user = User.objects.filter(pk=business_user_id).first()
        if not business_user:
            return Response(
                {"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND
            )

        orders = Order.objects.filter(business_user=business_user, status="in_progress")
        order_count = orders.count()
        return Response({"order_count": order_count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """
    Gibt die Anzahl der abgeschlossenen Bestellungen eines spezifischen Geschäftsnutzers zurück.
    - `GET`: Zählt die abgeschlossenen Bestellungen eines Geschäftsnutzers.
    """    
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        business_user_id = kwargs.get("pk")

        business_user = User.objects.filter(pk=business_user_id).first()
        if not business_user:
            return Response(
                {"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND
            )

        orders = Order.objects.filter(business_user=business_user, status="completed")
        order_count = orders.count()
        return Response(
            {"completed_order_count": order_count}, status=status.HTTP_200_OK
        )
