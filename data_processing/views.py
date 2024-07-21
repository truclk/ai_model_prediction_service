from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from data_processing.models import DatasetPreprocessed
from data_processing.models import DatasetRun
from data_processing.serializers import DatasetPreprocessedSerializer
from data_processing.serializers import DatasetRunSerializer
from data_processing.tasks.feature_selection import run_feature_selection


# Create your views here.
class DatasetPreprocessedViewSet(viewsets.ModelViewSet):
    queryset = DatasetPreprocessed.objects.all()
    serializer_class = DatasetPreprocessedSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("client_id", "dataset_upload_id")

    def get_queryset(self):
        return DatasetPreprocessed.objects.filter(client_id=self.request.session.get("client_id"))


class DatasetRunViewSet(viewsets.ModelViewSet):
    queryset = DatasetRun.objects.all()
    serializer_class = DatasetRunSerializer

    def get_queryset(self):
        return DatasetRun.objects.filter(client_id=self.request.session.get("client_id"))

    @action(detail=True, methods=["get", "post"])
    def detect_features(self, request, pk=None):
        try:
            dataset_run = DatasetRun.objects.get(id=pk)
        except DatasetRun.DoesNotExist:
            return Response({"error": "DatasetRun not found"}, status=status.HTTP_404_NOT_FOUND)
        run_feature_selection.delay(
            dataset_run.dataset_preprocessed.id, dataset_run.feature_selection_method, dataset_run.n_features_to_select
        )
        return Response({"message": "Feature selection started"}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post"])
    def train(self, request, pk=None):
        try:
            dataset_run = DatasetRun.objects.get(id=pk)
        except DatasetRun.DoesNotExist:
            return Response({"error": "DatasetRun not found"}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        client_id = self.request.session.get("client_id")
        serializer.save(client_id=client_id)
