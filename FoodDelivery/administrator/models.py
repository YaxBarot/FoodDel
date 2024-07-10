from django.db import models

# Create your models here.
from common.models import Audit


class Administrator(Audit):
    class Meta:
        db_table = 'fd_admin'

    id = models.BigAutoField(primary_key=True)

    email = models.EmailField(unique=True)
    password = models.TextField()




