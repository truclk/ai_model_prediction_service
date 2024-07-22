from rest_framework import serializers

from backend_api.models import DatasetMetadata
from backend_api.models import DatasetUpload
from backend_api.models import TrainningRun


class TrainningRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainningRun
        fields = "__all__"


class DatasetMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetMetadata
        fields = "__all__"
        read_only_fields = ["id", "user", "client"]


class DatasetUploadSerializer(serializers.ModelSerializer):
    metadata = DatasetMetadataSerializer(read_only=True)

    class Meta:
        model = DatasetUpload
        fields = "__all__"
        read_only_fields = ["id", "user", "client", "dataset_file"]


class PreprocessDataConfigSerializer(serializers.Serializer):
    columns = serializers.JSONField()
    predict_column = serializers.CharField()

    def validate_columns(self, value):
        # Add any custom validation logic for the columns field if necessary
        return value
