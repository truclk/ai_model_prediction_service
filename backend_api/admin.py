from data_processing.models import DatasetRunResult
from django.contrib import admin

from backend_api import models

# class DatasetResultAdmin(admin.ModelAdmin):
#     list_display = (
#         "get_dataset_upload",
#         "notebook_name",
#         "results",
#     )

#     def get_dataset_upload(self, obj):
#         return obj.dataset_upload.name

#     def get_dataset_upload_created(self, obj):
#         return obj.dataset_upload.created


class DatasetUploadAdmin(admin.ModelAdmin):
    list_display = ("name", "predict_column", "status")
    actions = ["detect_features", "process_dataset_upload"]

    # def process_dataset_upload(self, request, queryset):
    #     for dataset_upload in queryset:
    #         process_dataset_upload.delay(dataset_upload.id)

    def detect_features(self, request, queryset):
        for dataset_upload in queryset:
            # process_detect_features.delay(dataset_upload.id)
            pass


admin.site.register(models.Client)
admin.site.register(models.ClientUser)
admin.site.register(models.DatasetUpload, DatasetUploadAdmin)
# admin.site.register(DatasetRunResult, DatasetResultAdmin)


# Register your models here.
