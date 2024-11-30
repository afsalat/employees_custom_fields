from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import Employee
from customfields.models import CustomFieldData, Customfields

# Create your views here.

@api_view(['POST'])
def CreateEmployee(request):
    try:
        employee = request.POST

        
    except Exception as e:
        return Response({"error":str(e)}, status=500)
    

@api_view(['GET'])
def ViewAllEmployees(request):
    try:
        employee_list = Employee.objects.all()

        if not employee_list:
            return Response({"message":"employees not founded"})


        employee_data = [{"basic_details":employee_list}]
        for employee in employee_list:
            dynamic_field_data = CustomFieldData.objects.filter(employee_id=employee.id).all()
            for dynamic_field in dynamic_field_data:
                field = Customfields.objects.get(dynamic_field.field_id)
                employee_data.append({"field_name":field, "value": dynamic_field.value})

        return Response({"message":employee_data}, status=200)


    except Exception as e:
        return Response({"error":str(e)}, status=500)