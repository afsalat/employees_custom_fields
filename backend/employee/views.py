from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from customfields.models import CustomFieldData, Customfields

# Create Employee view (Using GET and POST for the form submission)
def create_employee(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            contact = request.POST.get('contact')
            # Add other fields as needed
            # Create the employee
            employee = Employee.objects.create(emp_name=name, emp_contact=contact)

            # Handle custom fields if any
            custom_fields = request.POST.getlist('custom_fields')  # Assuming custom fields are passed as a list
            for field_data in custom_fields:
                # Assuming custom_fields contains field_id and value in some format
                field_id, value = field_data.split(':')  # Example: field_id:value
                CustomFieldData.objects.create(employee=employee, field_id=field_id, value=value)

            return redirect('employee_list')  # Redirect to employee list after creating

        except Exception as e:
            return render(request, 'dashboard/emp_create.html', {'error': str(e)})

    # If GET request, render employee creation form
    return render(request, 'dashboard/emp_create.html')


# View All Employees (GET request)
def view_all_employees(request):
    try:
        employee_list = Employee.objects.all()

        if not employee_list:
            return render(request, 'dashboard/emp_list.html', {"message": "No employees found"})

        employee_data = []
        for employee in employee_list:
            employee_info = {"id": employee.id, "name": employee.name, "position": employee.position}
            dynamic_field_data = CustomFieldData.objects.filter(employee=employee)

            for field_data in dynamic_field_data:
                field = Customfields.objects.get(id=field_data.field_id)
                employee_info[f"field_{field.id}"] = {"field_name": field.name, "value": field_data.value}

            employee_data.append(employee_info)
            print(employee_info)

        return render(request, 'dashboard/emp_list.html', {"employees": employee_data})

    except Exception as e:
        return render(request, 'dashboard/emp_list.html', {'error': str(e)})


# Delete Employee (Using employee_id)
def delete_employee(request, employee_id):
    try:
        employee = get_object_or_404(Employee, id=employee_id)

        # Delete related dynamic fields first
        CustomFieldData.objects.filter(employee=employee).delete()

        # Delete the employee itself
        employee.delete()

        return redirect('employee_list')  # Redirect to employee list after deletion

    except Exception as e:
        return render(request, 'dashboard/emp_list.html', {'error': str(e)})
