from django.shortcuts import render
from django.http import HttpResponse
from .models import DemoItem

def index(request):
    items = DemoItem.objects.all()[:10]
    return render(request, 'core/index.html', {'items': items})
