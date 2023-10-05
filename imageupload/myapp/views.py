from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def image(request, pk):
    return JsonResponse('Image links', safe = False)

def images(request):
    return JsonResponse('Images List', safe = False)

def upload(request):
    return JsonResponse('Upload', safe = False)



