from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomFieldCreation
from .models import Customfields, CustomFieldData
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomFieldCreation
from .models import Customfields

@csrf_exempt  # This is to bypass CSRF verification for now (consider adding CSRF handling if needed)
def create_custom_field(request):
    if request.method == 'POST':
        try:
            # Get the JSON data from the request
            data = json.loads(request.body)

            # Loop through each field in the data and create the corresponding custom field
            for field in data.get('fields', []):
                # Assuming 'label' and 'field_type' are the keys for field data
                label = field.get('label')
                field_type = field.get('field_type')
                options = field.get('options', '')  # Options will be a comma-separated string if it's a select field

                # Create a new CustomField instance (replace CustomField with your actual model)
                new_field = CustomField(
                    label=label,
                    field_type=field_type,
                    options=options
                )
                new_field.save()

            # Respond with success
            return JsonResponse({'success': True}, status=200)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    # Handle GET or other requests (can be modified based on your needs)
    form = CustomFieldCreation()
    return render(request, 'dashboard/customfield.html', {'form': form})


# Update Custom Field view
def update_custom_field(request, field_id):
    try:
        field = get_object_or_404(Customfields, id=field_id)

        # Check if the field is used in CustomFieldData
        if CustomFieldData.objects.filter(field_id=field.id).exists():
            return render(request, 'dashboard/customfield.html', {"message": "Sorry, you can't update this field as it is already used. Please delete the associated employee first."})

        if request.method == 'POST':
            field_name = request.POST.get('field_name')
            field_type = request.POST.get('field_type')
            is_required = request.POST.get('is_required')

            field.field_name = field_name
            field.field_type = field_type
            field.is_required = is_required
            field.save()

            return redirect('custom_field_list')  # Redirect to the list of custom fields

        return render(request, 'dashboard/customfield.html', {'field': field})

    except Exception as e:
        return render(request, 'dashboard/customfield.html', {'message': str(e)})

# Delete Custom Field view
def delete_custom_field(request, field_id):
    try:
        field = get_object_or_404(Customfields, id=field_id)

        # Check if the field is used in CustomFieldData
        if CustomFieldData.objects.filter(field_id=field.id).exists():
            return render(request, 'dashboard/customfield.html', {"message": "Sorry, you can't delete this field as it is already used. Please delete the associated employee first."})

        field.delete()
        return redirect('custom_field_list')  # Redirect to the list after deletion

    except Exception as e:
        return render(request, 'dashboard/customfield.html', {'message': str(e)})

# View all Custom Fields
def view_all_custom_fields(request):
    try:
        fields = Customfields.objects.all()

        if fields:
            return render(request, 'dashboard/customfield.html', {'fields': fields})
        else:
            return render(request, 'dashboard/customfield.html', {'message': "No fields found."})

    except Exception as e:
        return render(request, 'dashboard/customfield.html', {'message': str(e)})
