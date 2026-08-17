from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Registers a new user (LANDLORD or TENANT). Publicly accessible.
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Takes email and password, returns JWT access and refresh tokens.
    """
    pass


class RefreshView(TokenRefreshView):
    """
    POST /api/auth/refresh/
    Takes a valid refresh token and returns a new access token.
    """
    pass


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Blacklists the provided refresh token to log the user out.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token is required."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        
        except TokenError:
            return Response(
                {"detail": "Token is invalid or already blacklisted."}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class UserMeView(generics.RetrieveUpdateAPIView):
    """
    GET /api/auth/me/
    PATCH /api/auth/me/
    Retrieves or updates the currently authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        # Override get_object to always return the user making the request
        return self.request.user