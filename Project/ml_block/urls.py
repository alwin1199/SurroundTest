from django.urls import path
from ml_block import views

urlpatterns = [
    path('', views.ml_block, name='ml_block'),
]