from data_processing.tasks.analyze_metadata import analyze_metadata
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from frontend.forms import FileUploadForm


@login_required
def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            dataset_upload = form.save(commit=False)
            dataset_upload.client_id = request.session.get("client_id")
            dataset_upload.user = request.user
            dataset_upload.save()
            # Trigger the analyze_metadata task
            analyze_metadata.delay(dataset_upload.id)
            # Redirect or show a success message after saving
            return redirect("dataset_detail", dataset_id=dataset_upload.id)
    else:
        form = FileUploadForm()
    return render(request, "dataset/upload.html", {"form": form})
