from django.urls import path

from .views import DatasetCatalog, DatasetExportAPI, PdfExportAPI

urlpatterns = [
    path(route="projects/<int:project_id>/download-format", view=DatasetCatalog.as_view(), name="download-format"),
    path(route="projects/<int:project_id>/download", view=DatasetExportAPI.as_view(), name="download-dataset"),
	path(route="projects/<int:project_id>/download-pdf", view=PdfExportAPI.as_view(), name="download-pdf"),
]
