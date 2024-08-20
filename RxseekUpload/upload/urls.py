from django.urls import path
from .views import upload_csv

urlpatterns = [
    path('medinfo/', upload_csv, name='upload_csv'),
]
