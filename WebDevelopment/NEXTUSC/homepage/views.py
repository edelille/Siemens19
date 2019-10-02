from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def homepage(request):
    #template = loader.get_template('homepage/index.html')
    return render(request, 'homepage/landingpage.html')

def oldHomepage(request):
    return render(request, 'homepage/oldhomepage.html')

def FourDisplayScreens(request):
    return render(request, 'homepage/fourdisplayscreens.html')
