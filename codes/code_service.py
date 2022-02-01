from typing import Union

import pandas as pd
from django.http import Http404
from django.utils import timezone
from rest_framework.request import Request

from codes.code_serializer import CodeSerializer, FileUploadSerializer
from codes.models import IcdCodeRecord
from users.models import User
from utility.api_helper import api_response


class CodeService:

    @staticmethod
    def list_codes():
        try:
            codes = IcdCodeRecord.objects.filter(status='ACTIVE').order_by('-created_at')
            return CodeSerializer(codes, many=True)
        except Exception as e:
            print(f"something went wrong {e}")

        # return serialized

    @staticmethod
    def create_record(request: Request, data: dict = None) -> CodeSerializer:

        serialized = CodeSerializer(data=request.data)

        if data:
            serialized = CodeSerializer(data=data)

        try:
            if serialized.is_valid(raise_exception=True):
                serialized.save(created_by=request.user)
        except Exception as e:
            print(f"Something went wrong {e}")

        return serialized

    @staticmethod
    def get_code(pk: str) -> CodeSerializer:
        try:
            code = CodeService.__get_object(pk)
            return CodeSerializer(code)
        except Http404:
            return api_response(404, "Record not found")
        except Exception as e:
            print(f"Something went wrong {e}")

    @staticmethod
    def update_code(pk: str, request: Request) -> Union[CodeSerializer, str]:
        code = CodeService.__get_object(pk)
        serialized = CodeSerializer(code, data=request.data, partial=True)
        try:
            if serialized.is_valid():
                serialized.save(updated_by=request.user, updated_at=timezone.now())
        except Exception as e:
            print(f"Something went wrong {e}")

        return serialized

    @staticmethod
    def delete_code(pk: str, user: User) -> bool:
        code = CodeService.__get_object(pk)
        data = {}

        serialized = CodeSerializer(code, data=data, partial=True)
        try:
            if serialized.is_valid():
                serialized.save(status="DELETED", deleted_at=timezone.now(), deleted_by=user)
                return True
        except Exception as e:
            print(f"Something went wrong {e}")

    @staticmethod
    def upload_csv(request: Request):
        resp = []
        serialized = FileUploadSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            file = serialized.validated_data['file']
            reader = pd.read_csv(file)
            for _, row in reader.iterrows():
                data = {
                    "icd_code": row["icd_code"],
                    "description": row["description"],
                    "icd_code_prefix": row["icd_code_prefix"],
                    "category": row["category"]
                }
                serialized = CodeService.create_record(request, data)

                if serialized.errors:
                    resp.append({"icd_code": data['icd_code'], "errors": serialized.errors})

                else:
                    resp.append(({"data": serialized.data}))

        return resp

    @staticmethod
    def __get_object(pk: str) -> IcdCodeRecord:
        try:
            return IcdCodeRecord.objects.get(pk=pk, status='ACTIVE')
        except IcdCodeRecord.DoesNotExist:
            raise Http404
            # raise api_response(status.HTTP_404_NOT_FOUND, "Record not found")
