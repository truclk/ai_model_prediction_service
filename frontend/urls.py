# urls.py
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()


urlpatterns = [
    # path("", include(router.urls)),
    path("", views.home_view, name="home_view"),
    path("upload/", views.upload_file, name="upload_file"),
    path("account/", views.account, name="account"),
    path("dataset/", views.dataset_list, name="dataset_list"),
    path("dataset/<int:dataset_id>/", views.dataset_detail, name="dataset_detail"),
    path("dataset/<int:pk>/preprocess/", views.PreprocessConfigView.as_view(), name="preprocess_form"),
    path("dataset/<int:pk>/preprocess_list/", views.PreprocessListView.as_view(), name="preprocess_list"),
    path(
        "dataset_preprocess/<int:dataset_preprocessed_id>/",
        views.DatasetPreprocessView.as_view(),
        name="dataset_run_form",
    ),
    path(
        "dataset_preprocess/<int:dataset_preprocessed_id>/create_run/",
        views.DatasetRunCreateView.as_view(),
        name="dataset_run_form",
    ),
    path("dataset_run/<int:dataset_run_id>/", views.DatasetRunView.as_view(), name="dataset_run_view"),
    path("dataset_run/<int:dataset_run_id>/edit/", views.DatasetRunEditView.as_view(), name="dataset_run_edit"),
    path("dataset_run/", views.DatasetRunListView.as_view(), name="dataset_run_list"),
    path(
        "dataset_run/<int:dataset_run_id>/results/",
        views.DatasetRunResultListView.as_view(),
        name="dataset_run_result_list",
    ),
    path("dataset_form/<int:pk>/", views.DatasetDetail.as_view(), name="dataset_form"),
    path(r"login/", views.user_login, name="user_login"),
    path(r"logout/", views.user_logout, name="user_logout")
    # Add other paths as necessary
]
