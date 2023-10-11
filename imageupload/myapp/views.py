from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Image, Profile, ExpiringLink
from .utils import manage_images
from .serializers import LoginUserSerializer, UploadImageSerializer, UpdateImageSerializer, GnerateExpiringLinkSerializer
from PIL import Image as PILImage

# Create your views here.
def image(request, pk, size):
	return manage_images(request, size, pk)

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
		logout(request)
		return Response({'message': 'Logged out successfully.'}, status=200 )
	
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
    return Response(image_list, status=200)


class UploadImageAPIView(APIView):
    serializer_class = UploadImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        owner = self.request.user
        tier = Profile.objects.get(user=request.user).tier
        image = request.data.get('image', None)
        title = request.data.get('title', None)
        description = request.data.get('description', None)
        sizes = tier.sizes.all().values_list('size', flat=True)
        accepted_formats = ('JPEG', 'PNG')
        links=[]
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
        
        image_obj = Image.objects.create(owner=owner, image=image, title=title, description=description, tier=tier)

        if tier.generate_expiring_link:
            for size in sizes:
                link = f"Your link for {'original' if size == 0 else f'{size}px'} image: images/{image_obj.id}/{size}"
                links.append(link)
                link = f"To generate expiring link for {'original' if size == 0 else f'{size}px'} image access: generate_exp_link/{image_obj.id}/{size}"
                links.append(link)
        else:
            for size in sizes:
                link = f"Your link for {'original' if size == 0 else f'{size}px'} image: images/{image_obj.id}/{size}"
                links.append(link)
        
        return Response({'message': links})


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


class GenerateExpiringLinkAPIView(APIView):
    serializer_class = GnerateExpiringLinkSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, size):
        user_profile = Profile.objects.get(user=request.user)
        user_tier = user_profile.tier

        if not user_tier.generate_expiring_link:
            return Response({'message': 'This user is not allowed to generate expiring links'}, status=403) 
        else:
            return Response({'message': 'Please insert seconds between 300 and 30000 for expiring link duration'}, status=200)     

    def post(self, request, pk, size):
        owner = self.request.user
        image = Image.objects.get(pk=pk)
        seconds = request.data.get('seconds', None)
        expiration_seconds = int(seconds) if seconds is not None else 0
        token = ExpiringLink.generate_link(image, expiration_seconds)
        link = f"exp_link/{pk}/{size}?token={token}"  
        return JsonResponse({'link': link})
         

def validate_expiring_link(request, pk, size):
    token = request.GET.get('token', None)
    if token:
        expiring_link = ExpiringLink.objects.filter(token=token).first()
        if expiring_link and expiring_link.expiration_timestamp > timezone.now():
            return manage_images(request, size, pk)
    return JsonResponse({'message': 'Invalid or expired link'}, status=400)