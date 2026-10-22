from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    """Vista de bienvenida de app tasks."""
    return HttpResponse("""
        <html>
            <body>
                <h1>TaskFlow</h1>
                <p>Bienvenido al sistema</p>
            </body>
        </html>
    """)


def home(request):
    """Vista de bienvenida de la app tasks."""
    return HttpResponse("Hola, TaskFlow")

def register(request):
    """Registro de usuarios"""
    return HttpResponse("Registro de usuario en Linea")

def perfil(request):
    """Perfil del usuario"""
    return HttpResponse("PERFIL DEL USUARIO")

def about_me(requets):
    """SOBRE MI"""
    return HttpResponse("Estudiante de la carrera tecnologica Desarrollo  en Software:  Mayte Rochina")

def greeting(request, nombre):
    """Registro usuarios"""
    return HttpResponse(
        f"Hola {nombre}, bienbenido a TaskFlow"
    )

def destination(request, titulo, nombre, cargo):
    """Registro usuario"""
    return HttpResponse(
        f"Bienvenido: {titulo} {nombre}, su cargo es: {cargo}"
    )

def base_triangulo(request, base, altura):
    """Registro usuario"""
    resultado =base*altura/2
    return HttpResponse(
        f"El àrea de un triagulo es: {resultado}")

def my_first_template(request):
    contexto = {
        "titulo": "TaskFlow",
        "mensaje": "Organiza tus proyectos y tareas en un solo lugar",
    }
    return render(request, "tasks/my-first-template.html", contexto)

def leads_like(request):
    contexto = {
        "titulo": "Tecnico",
        "nombre":"Mayte",
        "apellido": "Rochina",
    }
    return render(request,
                  "leads/leads-like.html", contexto
                  )