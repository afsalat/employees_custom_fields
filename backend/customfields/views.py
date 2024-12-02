from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomFieldCreation
from .models import Customfields, CustomFieldData
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomFieldCreation
from .models import Customfields
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Customfields  # Replace with your actual model import
from .forms import CustomFieldCreation  # Replace with your actual form import
import json
from django.core.exceptions import ValidationError

import logging

logger = logging.getLogger(__name__)  # Configure this in your settings

@csrf_exempt
def create_custom_field(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fields = data.get('fields', [])

            if not fields:
                return JsonResponse({'success': False, 'error': 'No fields provided'}, status=400)

            for field in fields:
                label = field.get('label')
                field_type = field.get('field_type')
                options = field.get('options', '')

                if not label or not field_type:
                    return JsonResponse({'success': False, 'error': 'Label and field type are required'}, status=400)

                new_field = Customfields(
                    field_name=label,
                    field_type=field_type,
                    is_required="yes"
                )
                new_field.full_clean()
                new_field.save()

            return JsonResponse({'success': True, 'message': 'Fields created successfully'}, status=201)
        
        except Exception as e:
            logger.error("Unhandled exception: %s", str(e))
            return JsonResponse({'success': False, 'error': 'Server error'}, status=500)

    return render(request, 'dashboard/customfield.html')




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
