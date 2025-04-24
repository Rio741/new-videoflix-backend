from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .serializers import RegistrationSerializer, LoginSerializer, PasswordResetConfirmSerializer
from ..models import User
from content_app.emails import send_password_reset_email, send_verification_email
import uuid


class RegistrationView(APIView):
    """
    Handles user registration. Sends a verification email after successful registration.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful! Please verify your email."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(APIView):
    """
    Handles user login. Returns an authentication token upon successful login.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'email': user.email,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    """
    Verifies the user's email address using the provided token.
    """
    permission_classes = [AllowAny]

    def get(self, request, token):
        user = get_object_or_404(User, verification_token=token)

        if user.is_active:
            return Response({"message": "Your account is already activated."}, status=status.HTTP_200_OK)

        user.is_active = True
        user.verification_token = None
        user.save()

        return Response({"message": "Email verified successfully! You can now log in."},
                        status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    """
    Initiates password reset by sending a reset token to the user's email.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
            reset_token = str(uuid.uuid4())
            user.verification_token = reset_token
            user.save(update_fields=["verification_token"])

            send_password_reset_email(user.email, reset_token)

        except User.DoesNotExist:
            pass

        return Response({"message": "If the email exists, a reset link has been sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Confirms the password reset by updating the user's password using the reset token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data["token"]
            new_password = serializer.validated_data["password"]
            user = get_object_or_404(User, verification_token=token)
            user.set_password(new_password)
            user.verification_token = None
            user.save()

            return Response({"message": "Password successfully reset! You can now log in."}, 
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResendConfirmationEmailView(APIView):
    """
    Resends the email verification link if the user has not yet confirmed their email.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required."}, status=400)

        user = get_object_or_404(User, email=email)

        if user.is_active:
            return Response({"message": "Your account is already activated."}, status=400)

        send_verification_email(user.email, user.verification_token)

        return Response({"message": "A confirmation email has been resent."}, status=200)
