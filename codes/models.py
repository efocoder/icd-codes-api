import uuid

from django.db import models

from users.models import Category, User
from utility.api_helper import STATUSES


class IcdCodeRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    icd_code = models.CharField(max_length=10, unique=True)
    icd_code_prefix = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUSES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    updated_at = models.DateTimeField(null=True, blank=True, default=None)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='%(class)s_requests_updated')
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='%(class)s_requests_deleted')

    def __str__(self):
        return f"{self.icd_code} - {self.description}"

    class Meta:
        db_table = "icd_code_records"
