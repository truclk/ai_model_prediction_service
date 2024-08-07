from rest_framework import serializers

from data_processing.models import DatasetPreprocessed
from data_processing.models import DatasetRun
from data_processing.models import DatasetRunResult


class DatasetPreprocessedSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset_upload.name", read_only=True)
    dataset_id = serializers.IntegerField(source="dataset_upload.id", read_only=True)
    run_count = serializers.SerializerMethodField()

    class Meta:
        model = DatasetPreprocessed
        fields = "__all__"
        read_only_fields = ["id", "dataset_upload", "client", "dataset_file"]

    def get_run_count(self, obj):
        return obj.datasetrun_set.count()


class DatasetRunSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source="dataset_preprocessed.dataset_upload.name", read_only=True)
    dataset_id = serializers.IntegerField(source="dataset_preprocessed.dataset_upload.id", read_only=True)
    dataset_preprocessed_id = serializers.IntegerField(source="dataset_preprocessed.id", read_only=True)
    number_of_results = serializers.SerializerMethodField()
    predict_column = serializers.CharField(source="dataset_preprocessed.predict_column", required=False)

    class Meta:
        model = DatasetRun
        fields = "__all__"
        read_only_fields = ["id", "client", "predict_column", "status"]

    def get_number_of_results(self, obj):
        return obj.datasetrunresult_set.count()

    def validate(self, data):
        # Check if the dataset_preprocessed is from the same client
        if "dataset_preprocessed" in data:
            dataset_preprocessed = data["dataset_preprocessed"]
            if not dataset_preprocessed:
                raise serializers.ValidationError("DatasetPreprocessed is required")
            if dataset_preprocessed.client.id != self.context["request"].session.get("client_id"):
                raise serializers.ValidationError("DatasetPreprocessed is not from the same client")
        return data


class DatasetRunResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetRunResult
        fields = "__all__"
        read_only_fields = ["id", "client", "status", "dataset_run"]
