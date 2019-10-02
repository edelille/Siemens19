from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='landingpage'),
    path('oldhomepage', views.oldHomepage, name='oldHomepage'),
    path('fourdisplayscreens', views.FourDisplayScreens, name='fourdisplayscreens'),
]
