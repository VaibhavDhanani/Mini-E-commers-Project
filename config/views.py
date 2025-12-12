from django.http.response import HttpResponse

def home_page(request):
    return HttpResponse('<h1>E-Commers App</h1>')