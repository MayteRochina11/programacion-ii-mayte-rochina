from django.shortcuts import render, redirect
from django.contrib import messages
from catalogo.forms.categoria_form import CategoriaForm
from catalogo.models import Categoria
from django.contrib.auth.decorators import login_required, permission_required
@login_required
@permission_required('catalogo.view_categoria', raise_exception=True)
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 
                  'catalogo/categorias/categoria_list.html', 
                  {'categorias': categorias})

@login_required
@permission_required('catalogo.add_categoria', raise_exception=True)
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 
                  'catalogo/categorias/formulario.html', 
                  {'form': form})

@login_required
@permission_required('catalogo.change_categoria', raise_exception=True)
def categoria_update(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 
                  'catalogo/categorias/formulario.html', 
                  {'form': form})

@login_required
@permission_required('catalogo.delete_categoria', raise_exception=True)
def categoria_delete(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('categoria_list')
    return render(request, 
                  'catalogo/categorias/categoria_confirm_delete.html', 
                  {'categoria': categoria})
