from django.db import models


class CvsModel(models.Model):
    variable = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
