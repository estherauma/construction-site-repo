from django.shortcuts import render,redirect
from .forms import WorkerForm,AttendanceForm
from .models import Worker,Attendance

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

def update_workers(request, pk):
    worker = Worker.objects.get(id=pk)
    form = WorkerForm(instance=worker)
    if request.method == 'POST':
        form = WorkerForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            return redirect('Tuzimbe:all-workers')
    return render(request, 'workers/update-workers.html', {'form': form})

def worker_details(request, pk):
    worker = Worker.objects.get(id=pk)
    return render(request, 'workers/worker-details.html', {'worker': worker})

def delete_workers(request, pk):
    worker = Worker.objects.get(id=pk)
    worker.delete()
    return redirect('Tuzimbe:all-workers')

def worker_attendance(request):
    form = AttendanceForm(request.POST)
    if request.method == 'POST':
        
        if form.is_valid():
            form.save()
            return redirect('Tuzimbe:all-workers')
    return render(request, 'workers/workers-attendance.html', {'form': form})

def attendance_list(request):
    attendance = Attendance.objects.all()
    return render(request, 'workers/attendance-list.html', {'attendances': attendance})
