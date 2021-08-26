from django.urls import path
from . import views

urlpatterns = [
    path('', views.queues_list,),
    path('<queue_pk>/', views.queue, name='queue'),
]