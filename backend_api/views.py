from rest_framework import viewsets

from backend_api.models import TrainningRun
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
