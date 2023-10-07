from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from .models import Image, Profile, Size, Tier
from .serializers import LoginUserSerializer
from PIL import Image as PILImage
from io import BytesIO

# Create your views here.
def image(request, pk, size):
    user_profile = Profile.objects.get(user=request.user)
    user_tier = user_profile.tier
    sizeObj = Size.objects.get(size=size)
    allowed_tiers = sizeObj.tier.all()
    print(user_tier)
    print(allowed_tiers)
    
    try:
        image_obj = Image.objects.get(pk=pk)
        if image_obj.image:
            if user_tier in allowed_tiers:
                if int(size) == 0:
                    return HttpResponse(image_obj.image.read(), content_type='image/jpeg')
                else:
                    # Open the image using PIL
                    image = PILImage.open(image_obj.image)

                    # Calculate the new height while maintaining the aspect ratio
                    new_height = int(size)
                    width_percent = (new_height / float(image.size[1]))
                    new_width = int((float(image.size[0]) * float(width_percent)))

                    # Resize the image
                    image = image.resize((new_width, new_height))

                    # Save the resized image to a BytesIO buffer in JPEG format
                    buffer = BytesIO()
                    image.save(buffer, format="JPEG")

                    # Move the buffer position to the start
                    buffer.seek(0)

                    # Return the resized image as an HTTP response
                    return HttpResponse(buffer.getvalue(), content_type='image/jpeg')
            else:
                return HttpResponse(status=404)
					
    except Image.DoesNotExist:
        pass

    return HttpResponse(status=404)

class loginUserAPIView(APIView):
	serializer_class = LoginUserSerializer
	authentication_classes = [SessionAuthentication]
	permission_classes = [AllowAny]
	# User is already logged

	def get(self, request):
		if request.user.is_authenticated:
			return HttpResponseRedirect('/images')
		else:
			return Response('Please login')
				
	def post(self, request):
		username = request.data.get('username', None)
		password = request.data.get('password', None)
		
		if not password:
			raise AuthenticationFailed('A user password is needed.')
		if not username:
			raise AuthenticationFailed('An username is needed.')
		
		user_instance = authenticate(request,username=username, password=password)
		
		if user_instance:
			if user_instance.is_active:
				login(request, user_instance)
				return HttpResponseRedirect('/images')
		if not user_instance:
			raise AuthenticationFailed('User not found.')
		    
		return Response({
			'message': 'Something went wrong.'
		})

class UserLogoutViewAPI(APIView):
	def get(self, request):
		response = Response()
		logout(request)
		response.data = {
                'message': 'Logged out successfully.'
            }
		return response
			
	
@api_view(['GET'])
@login_required
def images(request):
    # Retrieve a list images
    images = Image.objects.filter(owner=request.user)
    image_list = []
    # # Create list with user images
    for image in images:
        image_list.append(f"Image: {image.title} | Image description: {image.description} | Timestamp: {image.created} | Timestamp: {image.id}") 
    # Return the plain text response
    return Response(image_list)


def upload(request):
    return JsonResponse('Upload', safe = False)



