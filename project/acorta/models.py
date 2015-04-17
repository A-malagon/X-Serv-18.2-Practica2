from django.db import models

# Create your models here.

class AcortadorUrls(models.Model):
    URL = models.CharField(max_length=128)
