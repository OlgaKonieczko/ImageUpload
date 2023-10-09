from rest_framework import serializers
from .models import Image 

class LoginUserSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=100)
	password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})


class UploadImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Image
		fields = ('image','title', 'description')

class UpdateImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Image
		fields = ('image','title', 'description')

class GnerateExpiringLinkSerializer(serializers.Serializer):
	seconds= serializers.IntegerField(max_value=30000, min_value=30)
