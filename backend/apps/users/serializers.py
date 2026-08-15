from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the /api/auth/me/ endpoint.
    Restricts which fields a user can update themselves.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'role', 'created_at', 'updated_at']
        # Prevent users from changing their ID, email, role, or timestamps via PATCH
        read_only_fields = ['id', 'email', 'role', 'created_at', 'updated_at']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for the /api/auth/register/ endpoint.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'role']
        
    def validate_role(self, value):
        # Admin users should not be created via the public registration endpoint
        if value not in ['LANDLORD', 'TENANT']:
            raise serializers.ValidationError("Role must be either LANDLORD or TENANT.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user