from django.contrib.auth import get_user_model, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer


User = get_user_model()


class SignUp(generics.CreateAPIView):
    """Create an account."""
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer


class RequestToken(ObtainAuthToken):
    """Request an API token."""
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        # Get the user's username and password
        username = request.data.get('username')
        password = request.data.get('password')

        # Find any matching users
        user = authenticate(username=username, password=password)
        
        # Handle invalid login details
        if user is None:
            return Response({
                'message': 'Invalid username or password.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the user's token
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)


class DeleteToken(APIView):
    """Sign out and destroy access tokens."""

    def post(self, request):

        # Destroy any tokens for the currently authenticated user
        try:
            token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            pass
        else:
            token.delete()

        return Response(status=status.HTTP_200_OK)