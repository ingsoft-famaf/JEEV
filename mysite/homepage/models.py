from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyAdmin(AbstractBaseUser):

    is_admin = models.BooleanField(default=False)

    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
