# forms.py
from django import forms
from .models import DatasetUpload


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = DatasetUpload
        fields = ['name', 'dataset_file', 'predict_column']
