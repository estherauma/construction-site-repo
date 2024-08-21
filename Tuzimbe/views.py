from django.shortcuts import render,redirect
from .forms import WorkerForm
from .models import Worker

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
            return redirect('Tuzimbe:all-workers')
    else:
        form = WorkerForm()
    return render(request, 'workers/add-workers.html', {'form': form})

def all_workers(request):
    workers = Worker.objects.all()
    return render(request, 'workers/all-workers.html', {'workers': workers})
