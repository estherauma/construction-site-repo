from django.shortcuts import render,redirect
from .forms import WorkerForm

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def base(request):
    return render(request, 'pages/base.html')

def add_workers(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base')
    else:
        form = WorkerForm()
    return render(request, 'workers/add-workers.html')
