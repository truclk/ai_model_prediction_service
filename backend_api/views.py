from data_processing.tasks.preprocess_data import preprocess_data
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from backend_api.models import DatasetMetadata
from backend_api.models import DatasetUpload
from backend_api.models import TrainningRun
from backend_api.serializers import DatasetMetadataSerializer
from backend_api.serializers import DatasetUploadSerializer
from backend_api.serializers import PreprocessDataConfigSerializer
from backend_api.serializers import TrainningRunSerializer


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

    def get_queryset(self):
        return DatasetUpload.objects.filter(client_id=self.request.session.get("client_id"))

    @action(detail=True, methods=["get", "post"])
    def trigger_analyse(self, request, pk=None):
        # This would trigger the phase of pre-processing and analysis the metadata
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["get", "post"])
    def trigger_preprocess(self, request, pk=None):
        try:
            dataset_upload = DatasetUpload.objects.get(id=pk)
        except DatasetUpload.DoesNotExist:
            return Response({"error": "DatasetUpload not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PreprocessDataConfigSerializer(data=request.data)
        if serializer.is_valid():
            config = serializer.validated_data
            preprocess_data.delay(dataset_upload.id, config)
            return Response({"status": "Preprocessing started"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def metadata(self, request, pk=None):
        dataset_upload = self.get_object()
        metadata = dataset_upload.metadata.metadata  # Ensure this field exists and contains the metadata
        return Response(metadata)


class DatasetMetadataViewSet(viewsets.ModelViewSet):
    queryset = DatasetMetadata.objects.all()
    serializer_class = DatasetMetadataSerializer

    def get_queryset(self):
        return DatasetMetadata.objects.filter(client_id=self.request.session.get("client_id"))
