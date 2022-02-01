import threading

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from codes.code_service import CodeService
from utility.api_helper import api_response
from utility.email_service import EmailService
from utility.pagination_helper import CustomPagination


class CodesView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_classes = [CustomPagination]

    def get(self, _) -> Response:
        return api_response(status.HTTP_200_OK, 'Request successful', CodeService.list_codes().data)

    def post(self, request) -> Response:
        serialized = CodeService.create_record(request)

        print(serialized)
        if isinstance(serialized, str):
            return api_response(status.HTTP_400_BAD_REQUEST, serialized)

        elif serialized.errors:
            return api_response(status.HTTP_400_BAD_REQUEST, serialized.errors)

        return api_response(status.HTTP_200_OK, "Record created successfully", serialized.data)


class CodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _, pk):
        code = CodeService.get_code(pk)
        if code:
            return api_response(status.HTTP_200_OK, 'Request successful', code.data)

        return api_response(status.HTTP_404_NOT_FOUND, "Record not found")

    def patch(self, request, pk):
        serialized = CodeService.update_code(pk, request)
        if serialized.errors:
            return api_response(status.HTTP_400_BAD_REQUEST, serialized.errors)

        return api_response(status.HTTP_200_OK, 'Record updated successfully', serialized.data)

    def delete(self, request: Request, pk: str):
        if CodeService.delete_code(pk, request.user):
            return api_response(status.HTTP_204_NO_CONTENT, "Record deleted successfully")

        return api_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Sorry, something went wrong")


class UploadCsvView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = CodeService.upload_csv(request)
        emails_service = EmailService(request.user.email, "Upload Successful")
        threading.Thread(target=emails_service.send_upload_success, args=(len(data),)).start()
        return api_response(status.HTTP_200_OK, data)
