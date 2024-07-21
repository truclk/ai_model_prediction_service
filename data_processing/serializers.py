from rest_framework import serializers

from data_processing.models import DatasetPreprocessed
from data_processing.models import DatasetRun


class DatasetPreprocessedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetPreprocessed
        fields = "__all__"
        read_only_fields = ["id", "dataset_upload", "client", "dataset_file"]


class DatasetRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetRun
        fields = "__all__"
        read_only_fields = ["id", "client"]

    def validate(self, data):
        # Check if the dataset_preprocessed is from the same client
        dataset_preprocessed = data["dataset_preprocessed"]
        if not dataset_preprocessed:
            raise serializers.ValidationError("DatasetPreprocessed is required")
        if dataset_preprocessed.client != data["client"]:
            raise serializers.ValidationError("DatasetPreprocessed is not from the same client")
        return data
