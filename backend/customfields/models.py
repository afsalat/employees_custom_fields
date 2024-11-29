from django.db import models
from employee.models import Employee

# Create your models here.
class Customfields(models.Model):
    field_name = models.CharField(max_length=50, null=False)
    field_type = models.CharField(max_length=50, null=False)
    is_required = models.CharField(max_length=25, null=False)


class CustomFieldData(models.Model):
    field_id = models.ForeignKey(Customfields, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    value = models.TextField()