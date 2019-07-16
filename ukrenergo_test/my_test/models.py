from django.db import models


class CvsModel(models.Model):
    variable = models.CharField(max_length=50)
    alpha_a = models.CharField(max_length=50)
    alpha_b = models.CharField(max_length=50)
