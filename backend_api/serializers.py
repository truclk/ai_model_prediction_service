from rest_framework import serializers

from backend_api.models import TrainningRun, DatasetUpload, DatasetMetadata


class TrainningRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainningRun
        fields = "__all__"


class DatasetMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetMetadata
        fields = "__all__"


class DatasetUploadSerializer(serializers.ModelSerializer):
    datasetmetadata_set = DatasetMetadataSerializer(many=True, read_only=True)


    class Meta:
        model = DatasetUpload
        fields = "__all__"

    # Get nested model of DatasetMetadata
    # def to_representation(self, instance):
    #     self.fields['dataset_metadata'] = DatasetMetadataSerializer(read_only=True)
    #     return super(DatasetUploadSerializer, self).to_representation(instance)