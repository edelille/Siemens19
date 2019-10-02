'''
from django.urls import include, path
from djange.contrib import admin
from . import views

urlpatterns = {
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
}
'''
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
