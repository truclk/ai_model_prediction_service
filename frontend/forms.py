# forms.py
from backend_api.models import DatasetUpload
from django import forms


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = DatasetUpload
        fields = ["name", "dataset_file", "predict_column"]
