from django.shortcuts import render, redirect
from catalogo.models.libro import Libro
from catalogo.forms.libro_form import LibroForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('catalogo.view_libro', raise_exception=True)
def libro_list(request):
    pista = request.GET.get('pista', '').strip()
    categoria_id = request.GET.get('categoria_id', '').strip()
    libros = Libro.objects.select_related('categoria').all()
    if pista:
        libros = libros.filter(
            Q(titulo__icontains=pista) |
            Q(categoria__nombre__icontains=pista) |
            Q(autor__icontains=pista) |
        )
    if categoria_id:
        libros = libros.filter(categoria_id=categoria_id)
    categorias = Categoria.objects.all()
    contexto = {
        'libros': libros,
        'categorias': categorias,
        'pista': pista,
        'categoria_id': categoria_id,
    }

    return render(request, 
                  'catalogo/libros/libro_list.html', 
                  {'libros': libros}, contexto)

@login_required
@permission_required('catalogo.add_libro', raise_exception=True)
def create_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('libro_list')
    else:
        form = LibroForm()
    return render(request, 
                  'catalogo/libros/formulario.html', 
                  {'form': form})

@login_required
@permission_required('catalogo.change_libro', raise_exception=True)
def update_libro(request, pk):
    libro = Libro.objects.get(pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('libro_list')
    else:
        form = LibroForm(instance=libro)
    return render(request, 
                  'catalogo/libros/formulario.html', 
                  {'form': form})

@login_required
@permission_required('catalogo.delete_libro', raise_exception=True)
def delete_libro(request, pk):
    libro = Libro.objects.get(pk=pk)
    if request.method == 'POST':
        libro.delete()
        return redirect('libro_list')
    return render(request, 
                  'catalogo/libros/confirm_delete.html', 
                  {'libro': libro})
