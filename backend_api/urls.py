# urls.py
from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'dataset', views.DatasetUploadViewSet, basename="dataset_upoad")


urlpatterns = [
    path('', include(router.urls)),
    path('upload/', views.upload_file, name='upload_file'),
    # Add other paths as necessary
]
