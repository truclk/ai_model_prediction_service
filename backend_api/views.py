from rest_framework import viewsets

from backend_api.models import TrainningRun, DatasetUpload
from backend_api.serializers import TrainningRunSerializer, DatasetUploadSerializer
from django.shortcuts import render
from .forms import FileUploadForm


# Create your views here.
# This model viewset to create a run
class TrainningRunViewSet(viewsets.ModelViewSet):
    queryset = TrainningRun.objects.all()
    serializer_class = TrainningRunSerializer

    def create(self, request, *args, **kwargs):
        # This would create a run
        # This would submit a job to cluster
        # This would return the run id
        pass

    def retrieve(self, request, *args, **kwargs):
        # This would return the run status
        # This would return the run result
        pass

    def list(self, request, *args, **kwargs):
        # This would return the list of runs
        pass

    def update(self, request, *args, **kwargs):
        # This would update the run
        pass

    def partial_update(self, request, *args, **kwargs):
        # This would update the run
        pass

    def destroy(self, request, *args, **kwargs):
        # This would delete the run
        pass


class DatasetUploadViewSet(viewsets.ModelViewSet):
    queryset = DatasetUpload.objects.all()
    serializer_class = DatasetUploadSerializer


def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect or show a success message after saving
            return render(request, "success.html")
    else:
        form = FileUploadForm()
    return render(request, "upload.html", {"form": form})
