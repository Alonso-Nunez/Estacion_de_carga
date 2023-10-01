from django.shortcuts import render
def inicio(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

# Create your views here.
