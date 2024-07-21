# urls.py
from data_processing.views import DatasetPreprocessedViewSet
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"dataset", views.DatasetUploadViewSet, basename="dataset_upload")
router.register(r"preprocess", DatasetPreprocessedViewSet, basename="dataset_preprocessed")


urlpatterns = [
    path("", include(router.urls)),
    # Add other paths as necessary
]
