from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .serializers import RegistrationSerializer, LoginSerializer, PasswordResetConfirmSerializer
from ..models import User
from content_app.emails import send_password_reset_email
import uuid

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registrierung erfolgreich! Bitte bestätige deine E-Mail."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(APIView):
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
    permission_classes = [AllowAny]

    def get(self, request, token):
        user = get_object_or_404(User, verification_token=token)

        if user.is_active:
            return Response({"message": "Dein Konto wurde bereits aktiviert."}, status=status.HTTP_200_OK)

        user.is_active = True
        user.verification_token = None
        user.save()

        return Response({"message": "E-Mail erfolgreich bestätigt! Du kannst dich jetzt einloggen."},
                        status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
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

        return Response({"message": "Falls die E-Mail existiert, wurde eine Nachricht gesendet."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Diese View setzt das Passwort zurück, wenn der Benutzer das Formular mit dem Token abschickt.
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

            return Response({"message": "Passwort erfolgreich zurückgesetzt! Du kannst dich jetzt einloggen."}, 
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)