from .models import Image, Tier
from django.http import HttpResponse
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
                if int(size) == 0: #size 0 indicates orginal image size
                    return HttpResponse(image_obj.image.read(), content_type='image/jpeg')
                else:
                    image = PILImage.open(image_obj.image)
                    new_height = int(size)
                    width_percent = (new_height / float(image.size[1]))
                    new_width = int((float(image.size[0]) * float(width_percent)))
                    image = image.resize((new_width, new_height))

                    buffer = BytesIO()
                    image.save(buffer, format="JPEG")

                    buffer.seek(0)

                    return HttpResponse(buffer.getvalue(), content_type='image/jpeg')
            else:
               return HttpResponse(status=400)
					
    except Image.DoesNotExist:
        pass
    return HttpResponse(status=400)

def gen_links(image, sizes, tier):
    image_list = []
    if tier.generate_expiring_link:
        for size in sizes:
            link = f"Your link for {'original' if size == 0 else f'{size}px'} image: http://127.0.0.1:8000/images/{image.id}/{size}"
            image_list.append(link)
            link = f"To generate expiring link for {'original' if size == 0 else f'{size}px'} image go to: http://127.0.0.1:8000/generate_exp_link/{image.id}/{size}"
            image_list.append(link)
    else:
        for size in sizes:
            link = f"Your link for {'original' if size == 0 else f'{size}px'} image: http://127.0.0.1:8000/images/{image.id}/{size}"
            image_list.append(link)
    return image_list