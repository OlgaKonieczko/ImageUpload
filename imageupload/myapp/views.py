from django.http import HttpResponseRedirect
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
from .utils import manage_images, gen_links
from .serializers import LoginUserSerializer, UploadImageSerializer, UpdateImageSerializer, GnerateExpiringLinkSerializer
from PIL import Image as PILImage

        
def image(request, pk, size):
	return manage_images(request, size, pk)

@api_view(['GET'])
@login_required
def images(request):
    images = Image.objects.filter(owner=request.user)
    tier = Profile.objects.get(user=request.user).tier
    sizes = tier.sizes.all().values_list('size', flat=True)
    image_list = []
    for image in images:
        image_list.append(f"IMAGE: {image.title} | Image description: {image.description} | Timestamp: {image.created} | Image ID: {image.id}") 
        image_list.append(gen_links(image, sizes, tier))
    return Response(image_list)

@api_view(['GET','DELETE'])
@login_required(login_url='login')
def delete_image(request, pk):
    try:
        image = Image.objects.get(id=pk)
    except Image.DoesNotExist:
        return Response({'message': 'Image not found'}, status=404)

    if request.user != image.owner:
        return Response("You do not have permission to delete this image", status=403)
    else:
        image.delete()
        return Response({'message': 'Image deleted successfully.'})

def validate_expiring_link(request, pk, size):
    token = request.GET.get('token', None)
    if token:
        expiring_link = ExpiringLink.objects.filter(token=token).first()
        if expiring_link and expiring_link.expiration_timestamp > timezone.now():
            return manage_images(request, size, pk)
    return Response({'message': 'Invalid or expired link'}, status=400)

class loginUserAPIView(APIView):
	serializer_class = LoginUserSerializer
	authentication_classes = [SessionAuthentication]
	permission_classes = [AllowAny]
     
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

        if not image:
            return Response({'message': 'Please insert an image!'}, status=400)
        
        #check if inserted file is an image
        try:
            open_image = PILImage.open(image)
        except:
            return Response({'message': 'Unsupported image format!'}, status=400)
        
        if open_image.format not in accepted_formats:
            return Response({'message': 'Unsupported image format!'}, status=400)
        
        image_obj = Image.objects.create(owner=owner, image=image, title=title, description=description, tier=tier)
        links = gen_links(image_obj, sizes, tier)
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
        link = f"http://127.0.0.1:8000/exp_link/{pk}/{size}?token={token}"  
        return Response({'link': link})
         
