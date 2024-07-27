# urls.py
from data_processing.views import DatasetPreprocessedViewSet
from data_processing.views import DatasetRunResultViewSet
from data_processing.views import DatasetRunViewSet
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"dataset", views.DatasetUploadViewSet, basename="dataset_upload")
router.register(r"preprocess", DatasetPreprocessedViewSet, basename="dataset_preprocessed")
router.register(r"dataset_run", DatasetRunViewSet, basename="dataset_run")
router.register(r"dataset_run_result", DatasetRunResultViewSet, basename="dataset_run_result")


urlpatterns = [
    path("", include(router.urls)),
    # Add other paths as necessary
]
