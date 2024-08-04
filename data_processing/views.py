from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from data_processing.models import DatasetPreprocessed
from data_processing.models import DatasetRun
from data_processing.models import DatasetRunResult
from data_processing.serializers import DatasetPreprocessedSerializer
from data_processing.serializers import DatasetRunResultSerializer
from data_processing.serializers import DatasetRunSerializer
from data_processing.tasks.feature_selection import run_feature_selection
from data_processing.tasks.train import retrain_dataset_run
from data_processing.tasks.train import train_dataset_run


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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("client_id", "dataset_preprocessed_id")

    def get_queryset(self):
        return DatasetRun.objects.filter(client_id=self.request.session.get("client_id"))

    @action(detail=True, methods=["get", "post"])
    def detect_features(self, request, pk=None):
        try:
            dataset_run = DatasetRun.objects.get(id=pk)
        except DatasetRun.DoesNotExist:
            return Response({"error": "DatasetRun not found"}, status=status.HTTP_404_NOT_FOUND)
        run_feature_selection.delay(dataset_run.id)
        return Response({"message": "Feature selection started"}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["post"])
    def train(self, request, pk=None):
        try:
            dataset_run = DatasetRun.objects.get(id=pk)
            train_dataset_run.delay(dataset_run.id)

        except DatasetRun.DoesNotExist:
            return Response({"error": "DatasetRun not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Training started"}, status=status.HTTP_202_ACCEPTED)

    def perform_create(self, serializer):
        client_id = self.request.session.get("client_id")
        serializer.save(client_id=client_id)


class DatasetRunResultViewSet(viewsets.ModelViewSet):
    queryset = DatasetRunResult.objects.all()
    serializer_class = DatasetRunResultSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("client_id", "dataset_run_id")

    def get_queryset(self):
        return DatasetRunResult.objects.filter(client_id=self.request.session.get("client_id"))

    @action(detail=True, methods=["post"])
    def clone(self, request, pk=None):
        original_result = self.get_object()

        # Create a new instance with data from the original
        new_result_data = {
            "predict_column": original_result.predict_column,
            "number_of_features": original_result.number_of_features,
            "method": original_result.method,
            "features": original_result.features,
            "model": original_result.model,
            "parameters": request.data.get("parameters", original_result.parameters),
            "status": "PENDING",  # Set initial status to PENDING
        }

        serializer = self.get_serializer(data=new_result_data)
        if serializer.is_valid():
            serializer.save(dataset_run_id=original_result.dataset_run_id, client_id=original_result.client_id)
            retrain_dataset_run.delay(serializer.instance.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
