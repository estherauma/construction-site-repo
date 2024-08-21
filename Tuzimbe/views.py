from django.shortcuts import render, redirect, get_object_or_404
from .forms import MaterialsForm, UsageForm
from django.core.exceptions import ValidationError
from .models import Material, MaterialUsage
from .serializers import MaterialSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')

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