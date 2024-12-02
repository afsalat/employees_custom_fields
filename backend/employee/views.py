import json
import traceback
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from customfields.models import CustomFieldData, Customfields
from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm  # Assuming you have a form for basic employee data

def create_employee(request):
    if request.method == 'POST':
        try:
            # Handle basic fields
            form = EmployeeForm(request.POST)
            if form.is_valid():
                employee = form.save()  # Save basic employee fields

                # Handle custom fields
                custom_fields_data = json.loads(request.POST.get('custom_fields', '[]'))
                for field_data in custom_fields_data:
                    field_id = field_data.get('field_id')
                    value = field_data.get('value')
                    
                    if field_id and value:
                        CustomFieldData.objects.create(
                            employee=employee,
                            field_id=field_id,
                            value=value
                        )

                return redirect('view_all_employees')  # Redirect to employee list
            else:
                return render(request, 'dashboard/emp_create.html', {'form': form, 'error': form.errors})

        except Exception as e:
            return render(request, 'dashboard/emp_create.html', {'form': EmployeeForm(), 'error': str(e)})

    # Render the form with available custom fields
    form = EmployeeForm()
    custom_fields = Customfields.objects.all()
    return render(request, 'dashboard/emp_create.html', {'form': form, 'custom_fields': custom_fields})





def view_all_employees(request):
    try:
        employee_list = Employee.objects.all()
        print(f"Employee list: {employee_list}")  # Debug print

        if not employee_list:
            return render(request, 'dashboard/emp_list.html', {"message": "No employees found"})

        employee_data = []
        for employee in employee_list:
            print(f"Processing employee: {employee.emp_name}")  # Debug print
            employee_info = {"id": employee.id, "emp_name": employee.emp_name, "emp_contact": employee.emp_contact}
            print(employee.id)
            
            # Adjusted the query to use the correct field name for filtering
            dynamic_field_data = CustomFieldData.objects.filter(employee_id=employee.id)  # Assuming 'employee_id' is the correct field
            print(f"Dynamic field data: {dynamic_field_data}")  # Debug print
            
            if not dynamic_field_data:
                continue  # Skip if no custom fields for this employee

            for field_data in dynamic_field_data:
                field = Customfields.objects.get(id=field_data.field_id)
                field_name = f"field_{field.id}"
                employee_info[field_name] = {"field_name": field.field_name, "value": field_data.value}

            employee_data.append(employee_info)
            print(employee_data)

        return render(request, 'dashboard/emp_list.html', {"employees": employee_data})

    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print for any exceptions
        print("----",traceback.format_exc())
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
