from django.db import models

# Create your models here.

class Employee(models.Model):
    emp_name = models.CharField(max_length=50)
    emp_id = models.IntegerField()
    emp_contact = models.IntegerField()