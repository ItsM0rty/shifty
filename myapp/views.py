from django.shortcuts import render

def home(request):
    return render(request, 'myapp/index.html')

def about_view(request):
    return render(request, 'myapp/about.html', {})

def contact_view(request):
    return render(request, 'myapp/contact.html', {})

def sales_view(request):
    return render(request, 'myapp/sales.html', {})

def login_view(request):
    return render(request, 'myapp/login.html', {})
