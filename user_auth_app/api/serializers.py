from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from ..models import User
from content_app.emails import send_verification_email


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. Validates email and password confirmation.
    Sends a verification email after successful registration.
    """
    confirmedPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmedPassword']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """
        Ensures the email is unique for the user.
        """
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        """
        Validates that the password and confirmation password match.
        """
        if data['password'] != data['confirmedPassword']:
            raise ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Creates a new user and sends a verification email.
        """
        validated_data.pop('confirmedPassword')
        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'])
        send_verification_email(user.email, user.verification_token)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. Authenticates user with email and password.
    Ensures the account is active before login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validates user login credentials.
        """
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")

        if not user.is_active:
            raise serializers.ValidationError("Please verify your email first.")

        user = authenticate(username=user.email, password=password)

        if not user:
            raise serializers.ValidationError("Incorrect password.")

        data['user'] = user
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation. Validates the reset token and new password.
    """
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=6)
