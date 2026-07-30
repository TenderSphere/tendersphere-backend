from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)
    state = serializers.CharField(write_only=True)
    tender_interests = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'state', 'tender_interests']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        state = validated_data.pop('state')
        tender_interests = validated_data.pop('tender_interests')

        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user, phone=phone, state=state, tender_interests=tender_interests
        )
        return user