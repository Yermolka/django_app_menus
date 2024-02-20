from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index', kwargs={'item_name': None}),
    path('<str:item_name>/', views.index, name='index_with_item')
]