from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')

def add_workers(request):
    return render(request, 'workers/add-workers.html')
