from rest_framework import serializers

from backend_api.models import TrainningRun


class TrainningRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainningRun
        fields = "__all__"
