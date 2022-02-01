import uuid

from django.db import models

from utility.api_helper import STATUSES
from .user import User


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_code = models.CharField(max_length=6, unique=True)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUSES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='%(class)s_requests_deleted')

    def __str__(self):
        return self.description

    class Meta:
        db_table = "categories"
