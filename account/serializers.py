from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_confirm')
        if p1 != p2:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with such email already exists")
        return email

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)