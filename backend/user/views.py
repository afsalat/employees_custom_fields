from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm



@api_view(['POST'])
def Login(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({"refresh":str(refresh),
                            'access': str(refresh.access_token),
                            'status': 'success'
                            })
        else:
            return Response({"error":"Invalid credentials"}, status=400)

    except Exception as e:
        return Response({"error":str(e)}, status=500)
    


@api_view(['POST'])
def Register(request):
    try:
        user = UserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            return Response({'message':"successfully registered!!!"}, status=200)
        else:
            return Response({'message':"Please check the details"}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

