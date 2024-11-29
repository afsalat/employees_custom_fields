from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import CustomFieldCreation
from .models import Customfields, CustomFieldData



@api_view(['POST'])
def CreateCustomField(request):
    try:
        fields = CustomFieldCreation(request.POST)
        if fields.is_valid():
            fields.save()
            return Response({"message":"successfully created new field"}, status=200)
        else:
            return Response({"message":"Invalid data"}, status=400)
            
    except Exception as e:
        return Response({"error":str(e)}, status=500)
    



def UpdateCustomField(request, field_id):
    try:
        
        field_data = CustomFieldData.objects.get(field_id)
        if field_data is not None:
            return Response({"message":"Sorry, you can't update this field is already used. 'plesae delete employee first"}, 
                            status=200)

        field_name = request.POST.get('field_name')
        field_type = request.POST.get('field_type')
        is_required = request.POST.get('is_required')

        field = Customfields.objects.get(field_id)
        if field is not None:
            field.field_name = field_name
            field.field_type = field_type
            field.is_required = is_required
            field.save()

            return Response({"message":"successfully updated field"}, status=200)
        else:
            return Response({"message":"Invalid data"}, status=400)
        
    except Exception as e:
        return Response({"error":str(e)}, status=500)
    



def DeleteCustomField(request, field_id):
    try:
        
        field_data = CustomFieldData.objects.get(field_id)
        if field_data is not None:
            return Response({"message":"Sorry, you can't delete this field is already used. 'plesae delete employee first"}, 
                            status=200)

        field = Customfields.objects.get(field_id)

        if field is not None:
            field.delete()
            return Response({"message":"successfully deleted field"}, status=200)
        else:
            return Response({"message":"Invalid data"}, status=400)


    except Exception as e:
        return Response({"error":str(e)}, status=500)
    



@api_view(['POST'])
def ViewAllCustomField(request):
    try:

        fields = Customfields.objects.all()

        if fields is not None:
            return Response({"fields":fields}, status=200)
        else:
            return Response({"message":"field not founded"}, status=200)
        
    except Exception as e:
        return Response({"error":str(e)}, status=500)