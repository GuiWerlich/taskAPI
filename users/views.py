from rest_framework.views import APIView, Response, status
from .serializers import UserSerializer
from .serializers import CustomJWTSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        serializer = UserSerializer(user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer
