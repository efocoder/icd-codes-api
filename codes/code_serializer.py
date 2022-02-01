import re

from rest_framework import serializers

from codes.models import IcdCodeRecord
from users.category_serializer import CategorySerializer


class CodeSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True)

    class Meta:
        model = IcdCodeRecord
        fields = ('id', 'icd_code', 'description', 'status', 'created_at', 'icd_code_prefix', 'categories', 'category')
        extra_kwargs = {
            "categories": {
                "read_only": True
            },
            "category": {
                "write_only": True,
                "error_messages": {
                    "required": "Category required",
                    "blank": "Category required",
                }
            },
            "id": {"read_only": True},
            "status": {"read_only": True},
            "created_at": {"read_only": True},
            "icd_code": {
                "error_messages": {
                    "required": "Please provide icd code",
                    "blank": "Please provide icd code"
                }
            },
            "description": {
                "error_messages": {
                    "required": "Please provide icd code description",
                    "blank": "Please provide icd code description"
                }
            },

        }

    def validate_icd_code(self, icd_code):
        if not re.match("^[a-zA-Z0-9,. -]*$", icd_code):
            raise serializers.ValidationError(
                {"icd_code": "ICD code should contain letters, numbers, dash and spaces only"})

        return icd_code

    def validate_description(self, description):
        if not re.match("^[a-zA-Z0-9,. -]*$", description):
            raise serializers.ValidationError(
                {"description": "Description should contain letters, numbers, dash and spaces only"})

        return description

    def create(self, validated_data):
        return IcdCodeRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(validated_data)
        instance.icd_code = validated_data.get('icd_code', instance.icd_code)
        instance.description = validated_data.get('description', instance.description)
        instance.icd_code_prefix = validated_data.get('icd_code_prefix', instance.icd_code_prefix)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.status = validated_data.get('status', instance.status)
        instance.deleted_at = validated_data.get('deleted_at', instance.deleted_at)
        instance.deleted_by = validated_data.get('deleted_by', instance.deleted_by)

        instance.save()
        return instance


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file',)
