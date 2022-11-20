from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('insert_info', views.insert_info, name='insert_info'),
    path('add_task', views.add_task, name='add_task'),
    path('clean_database', views.clean_database, name='clean_database'),
    path('get_completion', views.get_completion, name='get_completion'),
    path('delete_logitems', views.delete_logitems, name='delete_logitems'),
    path('calculate_score', views.calculate_score, name='calculate_score'),
    path('add_key', views.add_key, name='add_key'),
    path('get_key', views.get_key, name='get_key'),
    path('test_key', views.test_key, name='test_key'),
    path('clean_key', views.clean_key, name='clean_key'),
    path('query_feature', views.query_feature, name='query_feature'),
    path('get_task', views.get_task, name='get_task'),
]