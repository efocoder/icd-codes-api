from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, status="ACTIVE"):
        user_object = self.model(
            email=self.normalize_email(email),
        )
        user_object.username = username
        user_object.first_name = first_name
        user_object.last_name = last_name
        user_object.status = status
        user_object.created_at = timezone.now()
        user_object.set_password(password)
        user_object.save(using=self._db)

        return user_object

    def create(self, email, username, first_name, last_name, password=None, *args, **kwargs):
        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            password=password
        )

        return user
