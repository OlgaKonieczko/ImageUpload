from .models import Image, Profile, Size, Tier, ExpiringLink
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from PIL import Image as PILImage
from io import BytesIO

def manage_images(request, size, pk):
    try:
        image_obj = Image.objects.get(pk=pk)
        imageTier = image_obj.tier
        tierObj = Tier.objects.get(tier=imageTier)
        sizes = tierObj.sizes.all().values_list('size', flat=True)
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
               return HttpResponse(status=400)
					
    except Image.DoesNotExist:
        pass

    return HttpResponse(status=400)
