from django.db import models

# Create your models here.
class TrainModel(models.Model):
    data_name = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50, null=True)
