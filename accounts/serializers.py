from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}, 
        }


    def validate_email(self, email):

        email = email.lower()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already in use.")
        
        return email

    
    def create(self, validated_data):

        # Create a user with an email and password
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Add any extra fields
        user.first_name = validated_data.get('first_name', '')
        user.last_name = validated_data.get('last_name', '')

        user.save()
        return user