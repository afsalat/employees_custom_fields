from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(['POST'])
def Login(request):
    try:
        pass
    except Exception as e:
        return Response({"error":str(e), })