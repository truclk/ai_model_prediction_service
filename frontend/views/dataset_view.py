from backend_api.models import DatasetUpload
from backend_api.serializers import DatasetUploadSerializer
from data_processing.models import DatasetRun
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


def dataset_list(request):
    return render(request, "dataset/list.html")


def dataset_detail(request, dataset_id):
    return render(request, "dataset/detail.html", {"dataset_id": dataset_id})


class DatasetDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "dataset/detail_form.html"

    def get(self, request, pk):
        dataset = get_object_or_404(DatasetUpload, pk=pk, client_id=request.session.get("client_id"))
        serializer = DatasetUploadSerializer(dataset)
        return Response({"serializer": serializer, "dataset": dataset})

    def post(self, request, pk):
        dataset = get_object_or_404(DatasetUpload, pk=pk, client_id=request.session.get("client_id"))
        serializer = DatasetUploadSerializer(dataset, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "dataset": dataset})
        serializer.save()
        return redirect("dataset_list")


class PreprocessListView(View):
    template_name = "dataset/preprocess_list.html"

    def get(self, request, pk):
        dataset = get_object_or_404(DatasetUpload, pk=pk, client_id=request.session.get("client_id"))
        metadata = dataset.metadata  # Assume metadata is already available in the dataset
        return render(request, self.template_name, {"dataset": dataset, "metadata": metadata})


class PreprocessConfigView(View):
    template_name = "dataset/preprocess_form.html"

    def get(self, request, pk):
        dataset = get_object_or_404(DatasetUpload, pk=pk, client_id=request.session.get("client_id"))
        metadata = dataset.metadata  # Assume metadata is already available in the dataset
        return render(request, self.template_name, {"dataset": dataset, "metadata": metadata})

    def post(self, request, pk):
        return redirect("dataset_detail", dataset_id=pk)


class DatasetRunCreateView(View):
    template_name = "dataset/run_form.html"

    def get(self, request, dataset_preprocessed_id):
        return render(request, self.template_name, {"dataset_preprocessed_id": dataset_preprocessed_id})


class DatasetRunView(View):
    template_name = "dataset/run_view.html"

    def get(self, request, dataset_run_id):
        dataset_run = get_object_or_404(DatasetRun, pk=dataset_run_id, client_id=request.session.get("client_id"))
        return render(request, self.template_name, {"dataset_run_id": dataset_run.id})


class DatasetRunEditView(View):
    template_name = "dataset/run_edit.html"

    def get(self, request, dataset_run_id):
        return render(
            request,
            self.template_name,
            {"dataset_run_id": dataset_run_id, "client_id": request.session.get("client_id")},
        )


class DatasetRunListView(View):
    template_name = "dataset/run_list.html"

    def get(self, request):
        client_id = request.session.get("client_id")
        return render(request, self.template_name, {"client_id": client_id})


class DatasetRunResultListView(View):
    template_name = "dataset/dataset_run_result_list.html"

    def get(self, request, dataset_run_id):
        context = {
            "dataset_run_id": dataset_run_id,
        }
        return render(request, self.template_name, context)
