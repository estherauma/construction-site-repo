from django.shortcuts import render, redirect, get_object_or_404
from .forms import WorkerForm,AttendanceForm,MaterialsForm,UsageForm
from django.core.exceptions import ValidationError
from .models import Material, MaterialUsage,Worker,Attendance
from .serializers import MaterialSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import WorkerSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.forms import UserCreationForm
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm



# Create your views here.

# API Views

class WorkerListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class WorkerDetailAPIView(APIView):
    def get(self,request, pk):
        try:
            worker = Worker.objects.get(pk=pk)
        except Worker.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WorkerSerializer(worker)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WorkerCreateAPIView(APIView):
    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WorkerUpdateAPIView(APIView):
    def get_object(self, pk):
        try:
            return Worker.objects.get(pk=pk)
        except Worker.DoesNotExist:
            return None

    def put(self, request, pk):
        worker = self.get_object(pk)
        if not worker:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WorkerSerializer(worker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        worker = self.get_object(pk)
        if not worker:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WorkerSerializer(worker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        worker = self.get_object(pk)
        if not worker:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        worker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterWorkerAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                "first_name": user.first_name,
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Template Views
def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('Tuzimbe:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'auth/signup.html', {'form': form})

def authView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Tuzimbe:all_workers')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def add_workers(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Tuzimbe:all_workers')
    else:
        form = WorkerForm()
    return render(request, 'workers/add_workers.html', {'form': form})

def all_workers(request):
    workers = Worker.objects.all()
    return render(request, 'workers/all_workers.html', {'workers': workers})

def update_workers(request, pk):
    worker = Worker.objects.get(id=pk)
    form = WorkerForm(instance=worker)
    if request.method == 'POST':
        form = WorkerForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            return redirect('Tuzimbe:all_workers')
    return render(request, 'workers/update_workers.html', {'form': form})

def worker_details(request, pk):
    worker = Worker.objects.get(id=pk)
    return render(request, 'workers/worker_details.html', {'worker': worker})

def delete_workers(request, pk):
    worker = Worker.objects.get(id=pk)
    worker.delete()
    return redirect('Tuzimbe:all_workers')

def worker_attendance(request):
    form = AttendanceForm(request.POST)
    if request.method == 'POST':
        
        if form.is_valid():
            form.save()
            return redirect('Tuzimbe:attendance_list')
    return render(request, 'workers/workers_attendance.html', {'form': form})

def attendance_list(request):
    attendance = Attendance.objects.all()
    return render(request, 'workers/attendance_list.html', {'attendances': attendance})

def update_attendance(request, pk):
    attendance = Attendance.objects.get(id=pk)
    form = AttendanceForm(instance=attendance)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('Tuzimbe:attendance_list')
    return render(request, 'workers/update_attendance.html', {'form': form})

def add_material(request):
    error_message = None
    if request.method == 'POST':
        form = MaterialsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('Tuzimbe:materials')
            except ValidationError as e:
                error_message = e.message
        else:
            error_message = form.errors
    else:
        form = MaterialsForm()
    return render(request, 'materials/add_materials.html', {'form': form, 'error_message': error_message})


def all_materials(request):
    material = Material.objects.all()
    return render(request, 'materials/all_materials.html', {'materials': material})

def details(request, id):
    material = get_object_or_404(Material, id=id)
    usage = MaterialUsage.objects.filter(material=material)
    return render(request, 'materials/details.html', {'material': material, 'usage': usage})


def edit_material(request, id):
    material = get_object_or_404(Material, id=id)
    error_message = None

    if request.method == 'POST':
        form = MaterialsForm(request.POST, instance=material)
        if form.is_valid():
            try:
                form.save()
                return redirect('Tuzimbe:details', id=material.id)
            except ValidationError as e:
                error_message = e.message
        else:
            return render(request, 'materials/edit_material.html', {'form': form, 'material': material})
    else:
        form = MaterialsForm(instance=material)
    return render(request, 'materials/edit_material.html', {'form': form, 'material': material, 'error_message': error_message})


def material_usage(request):
    if request.method == 'POST':
        form  = UsageForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('Tuzimbe:materials')
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = UsageForm()
    return render(request, 'materials/material_use.html', {'form': form})


class MaterialDetailView(RetrieveAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    lookup_field = 'id'

class MaterialAllView(APIView):
    def get(self, request):
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            try:
                material_name = serializer.validated_data.get('name')
                unit = serializer.validated_data.get('unit')
                total_quantity_stocked = serializer.validated_data.get('total_quantity_stocked')

                existing_material = Material.objects.filter(name=material_name, unit=unit).first()

                if existing_material:
                    existing_material.total_quantity_stocked += total_quantity_stocked
                    existing_material.total_price = existing_material.total_quantity_stocked * existing_material.price_per_unit
                    existing_material.save()
                    return Response({"message": "Material Quantity updated successfully"}, status=status.HTTP_200_OK)
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       


class MaterialDetailview(APIView):
    def get(self, request, id,):
        material = get_object_or_404(Material, id=id)
        serializer = MaterialSerializer(material)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, id, *args, **kwargs):
        material = get_object_or_404(Material, id=id)
        serializer = MaterialSerializer(material, data=request.data)
        if serializer.is_valid():
            try:
                if serializer.validated_data.get('total_quantity_stocked') < 0:
                    return Response({'error': 'Total quantity cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id, *args, **kwargs):
        material = get_object_or_404(Material, id=id)
        serializer = MaterialSerializer(material, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                if serializer.validated_data.get('total_quantity_stocked') is not None and serializer.validated_data.get('total_quantity_stocked') < 0:
                    return Response({'error': 'Total quantity cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, *args, **kwargs):
        try:
            material = Material.objects.get(id=id)
            material.delete()
            return Response({"message": "Material deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Material.DoesNotExist:
            return Response({"error": "Material not found."}, status=status.HTTP_404_NOT_FOUND)