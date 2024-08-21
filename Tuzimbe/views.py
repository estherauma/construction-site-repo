from django.shortcuts import render, redirect, get_object_or_404
from .forms import MaterialsForm, UsageForm
from django.core.exceptions import ValidationError
from .models import Material, MaterialUsage

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

