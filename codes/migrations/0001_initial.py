# Generated by Django 4.0.1 on 2022-01-30 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IcdCodeRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('icd_code', models.CharField(max_length=10, unique=True)),
                ('icd_code_prefix', models.CharField(blank=True, max_length=5, null=True)),
                ('description', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('DELETED', 'DELETED')], default='ACTIVE', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_requests_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_requests_deleted', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_requests_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'icd_code_records',
            },
        ),
    ]
