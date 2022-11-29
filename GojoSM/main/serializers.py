from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Following

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user_obj = User.objects.create_user(username= validated_data['username'], email=validated_data['email'], password=validated_data['password'])
        return user_obj

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'birth_date', 'country']

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ["follower", "followed"]