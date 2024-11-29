from django.contrib import admin
from .models import CustomFieldData, Customfields

# Register your models here.

admin.site.register(Customfields)
admin.site.register(CustomFieldData)
