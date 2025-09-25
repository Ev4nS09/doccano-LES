import io
import os
from celery.result import AsyncResult
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from data_export.pipeline.writers import PdfWriter

from .celery_tasks import export_dataset, export_to_pdf
from .pipeline.catalog import Options
from projects.models import Project
from projects.permissions import IsProjectAdmin
import tempfile  # For temporary file handling
import logging   # For error logging

logger = logging.getLogger(__name__)


class DatasetCatalog(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        project = get_object_or_404(Project, pk=project_id)
        use_relation = getattr(project, "use_relation", False)
        options = Options.filter_by_task(project.project_type, use_relation)
        return Response(data=options, status=status.HTTP_200_OK)


class DatasetExportAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        task_id = request.GET["taskId"]
        task = AsyncResult(task_id)
        ready = task.ready()
        if ready:
            filename = task.result
            return FileResponse(open(filename, mode="rb"), as_attachment=True)
        return Response({"status": "Not ready"})

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs["project_id"]
        file_format = request.data.pop("format")
        export_approved = request.data.pop("exportApproved", False)
        task = export_dataset.delay(
            project_id=project_id, file_format=file_format, confirmed_only=export_approved, **request.data
        )
        return Response({"task_id": task.task_id})

class PdfExportAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, request, project_id):
        try:
            # Create temp file
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Get the data from request body
            request_data = request.data
            print("Received data for PDF generation:", request_data)  # Debug log
            
            # Prepare the data structure for PdfWriter
            pdf_data = {
                'projectId': str(project_id),
                'generalStats': request_data.get('generalStats', {}),
                'perspectiveStats': request_data.get('perspectiveStats', {})
            }
            
            # Write to temp file
            with open(temp_path, 'wb') as f:
                success = PdfWriter.write(f, pdf_data)
                if not success:
                    raise ValueError("PDF generation failed")
            
            # Verify PDF content
            with open(temp_path, 'rb') as f:
                content = f.read()
                if not content.startswith(b'%PDF'):
                    raise ValueError("Generated file is not a valid PDF")
            
            # Return the file
            response = FileResponse(
                open(temp_path, 'rb'),
                content_type='application/pdf',
                as_attachment=True,
                filename=f'project_{project_id}_stats.pdf'
            )
            
            # Clean up the temp file after response is sent
            response['Content-Disposition'] = f'attachment; filename="project_{project_id}_stats.pdf"'
            return response
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(f"PDF export failed for project {project_id}: {str(e)}")
            return Response(
                {"error": f"PDF generation failed: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
