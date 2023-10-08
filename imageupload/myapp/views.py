from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Image, Profile, Size, Tier
from .serializers import LoginUserSerializer, UploadImageSerializer, UpdateImageSerializer
from PIL import Image as PILImage
from io import BytesIO

# Create your views here.
def image(request, pk, size):
    user_profile = Profile.objects.get(user=request.user)
    user_tier = user_profile.tier
    tierObj = Tier.objects.get(tier=user_tier)
    sizes = tierObj.sizes.all().values_list('size', flat=True)
	
    try:
        image_obj = Image.objects.get(pk=pk)
        if image_obj.image:
            if int(size) in sizes:
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
               #return JsonResponse('This user cannot acces image this size.', status=404, safe = False)
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
        image_list.append(f"Image: {image.title} | Image description: {image.description} | Timestamp: {image.created} | Image ID: {image.id}") 
    # Return the plain text response
    return Response(image_list)


class UploadImageAPIView(APIView):
    serializer_class = UploadImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        owner = self.request.user
        image = request.data.get('image', None)
        title = request.data.get('title', None)
        description = request.data.get('description', None)
        accepted_formats = ('JPEG', 'PNG')
        #check if file is inserted
        if not image:
            return Response({'message': 'Please insert an image!'}, status=400)
        
        #check if inserted file is an image
        try:
            open_image = PILImage.open(image)
        except:
            return Response({'message': 'Unsupported image format!'}, status=400)
        
        #check if inserted image is in accepted
        if open_image.format not in accepted_formats:
            return Response({'message': 'Unsupported image format!'}, status=400)
        
        image_obj = Image.objects.create(owner=owner, image=image, title=title, description=description)
        return Response({'message': 'Image uploaded.'})


class UpdateImageAPIView(APIView):
    serializer_class = UpdateImageSerializer

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return None
        
    def get(self, request, pk):
        image_obj = self.get_object(pk)
        if not image_obj:
            return Response({'message': 'Image not found.'}, status=404)
        
        if request.user != image_obj.owner:
            return Response({'message': 'You do not have permission to view this image.'}, status=403)
        
        # Serialize the existing image object and include it in the response
        serializer = self.serializer_class(image_obj)
        return Response(serializer.data)
    
    def post(self, request, pk):
        owner = self.request.user
        image = request.data.get('image', None)
        title = request.data.get('title', None)
        description = request.data.get('description', None)
        accepted_formats = ('JPEG', 'PNG')

        image_obj = self.get_object(pk)
        if not image_obj:
            return Response({'message': 'Image not found.'}, status=404)
        
        if request.user != image_obj.owner:
            return Response({'message': 'You do not have permission to update this image.'}, status=403)
        
        if image:
            try:
                open_image = PILImage.open(image)
            except:
                return Response({'message': 'Unsupported image format!'}, status=400)
            
            if open_image.format not in accepted_formats:
                return Response({'message': 'Unsupported image format!'}, status=400)
            image_obj.image = image
        if title:
            image_obj.title = title
        if description:
            image_obj.description = description
        image_obj.save()

        return Response({'message': 'Image updated successfully.'})


@api_view(['GET'])
@login_required(login_url='login')
def deleteImage(request, pk):
    try:
        image = Image.objects.get(id=pk)
    except Image.DoesNotExist:
        return Response({'message': 'Image not found'}, status=404)

    if request.user != image.owner:
        return HttpResponseForbidden("You do not have permission to delete this image")
    else:
        image.delete()
        return Response({'message': 'Image deleted successfully.'})