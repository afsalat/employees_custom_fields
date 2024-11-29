from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render


# Create your views here.

@api_view(['POST'])
def CreateEmployee(request):
    try:
        
    except Exception as e:
        return Response({"error":str(e)}, status=500)