from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField()
    branch = models.CharField(max_length=100)
    result = ArrayField(ArrayField(models.FloatField()))

    def __str__(self):
        return str(self.roll_no)
