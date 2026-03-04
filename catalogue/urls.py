from django.urls import path
from . import views
urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('livre/<int:pk>/', views.livre_detail, name='livre_detail'),
    path('recherche/', views.recherche, name='recherche')
]