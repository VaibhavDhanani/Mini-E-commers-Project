from django.http.response import HttpResponse

def home(request):
    return HttpResponse('<h1>E-Commers App</h1>')