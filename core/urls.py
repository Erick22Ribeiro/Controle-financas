from django.urls import path
from core import views

urlpatterns = [
    path('', views.financas, name='home'),
    path('dados/', views.dados, name='dados')
]