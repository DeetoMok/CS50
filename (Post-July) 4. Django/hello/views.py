from django.http import HttpResponse
from django.shortcuts import render

def index0(request):
    return HttpResponse("Hello, world!")

def index1(request):
    # prefix with hello to differentiate greet.html from hello app with greet.html from other apps
    return render(request, "hello/index.html")

def brian(request):
    return HttpResponse("Hello, Brian!")

def david(request):
    return HttpResponse("Hello, David!")

def greet0(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}!")

# Renders an entire html file instead of just a string
def greet1(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })