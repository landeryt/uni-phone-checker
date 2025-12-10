from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("This is the backend.")

def count(request):
    return HttpResponse("Phone count endpoint.")

def validate(request):
    return HttpResponse("Phone validation endpoint.")

def registration(request):
    return HttpResponse("User registration endpoint.")

