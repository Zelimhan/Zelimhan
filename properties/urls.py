from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:pk>/', views.property_detail, name='property_detail'),
    path('podbor/', views.selection, name='selection'),
    path('podbor/spasibo/', views.selection_thanks, name='selection_thanks'),
    path('contacts/', views.contacts, name='contacts'),
]
