from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer


class CustomLoginView(ObtainAuthToken):
    """
    Custom view for user login that extends the default ObtainAuthToken view. This view handles authentication requests,
    validating the user's credentials, and if valid, returns the user's token along with their username, email, and user ID.
    If the credentials are invalid, it returns an error response.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(APIView):
    """
    A view for user registration that handles the creation of new user accounts. It validates user data,
    creates a new user account if the data is valid, and issues a token for the newly created user. Successful registration
    results in a response containing the user's token, username, email, and user ID. Errors in data submission are returned as error responses.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save(request=request)
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                "token": token.key,
                "username": saved_account.username,
                "email": saved_account.email,
                "user_id": saved_account.id,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
