from rest_framework import serializers

class LoginUserSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=100)
	password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
