from django.urls import path
from core import views

urlpatterns = [
    path('', views.financas, name='home'),
    path('transacoes/', views.transacoes, name='transacoes'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),

]