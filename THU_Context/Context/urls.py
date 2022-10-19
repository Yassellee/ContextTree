from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('insert_info', views.insert_info, name='insert_info'),
    path('add_task', views.add_task, name='add_task'),
    path('clean_database', views.clean_database, name='clean_database'),
]