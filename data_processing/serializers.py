from rest_framework import serializers

from data_processing.models import DatasetPreprocessed
from data_processing.models import DatasetRun


class DatasetPreprocessedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetPreprocessed
        fields = "__all__"
        read_only_fields = ["id", "dataset_upload", "client", "dataset_file"]


class DatasetRunSerializer(serializers.ModelSerializer):
    dataset_name = serializers.SerializerMethodField()

    class Meta:
        model = DatasetRun
        fields = "__all__"
        read_only_fields = ["id", "client"]

    def get_dataset_name(self, obj):
        return obj.dataset_preprocessed.dataset_upload.name

    def validate(self, data):
        # Check if the dataset_preprocessed is from the same client
        if "dataset_preprocessed" in data:
            dataset_preprocessed = data["dataset_preprocessed"]
            if not dataset_preprocessed:
                raise serializers.ValidationError("DatasetPreprocessed is required")
            if dataset_preprocessed.client.id != self.context["request"].session.get("client_id"):
                raise serializers.ValidationError("DatasetPreprocessed is not from the same client")
        return data
