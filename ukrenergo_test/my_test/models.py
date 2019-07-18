from django.db import models


class CvsModel(models.Model):
    variable = models.CharField(max_length=50, null=True)
    value = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.variable
