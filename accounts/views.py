from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import (
    UserSerializer,
    StudentRegistrationSerializer,
    TeacherRegistrationSerializer,
    CustomTokenObtainPairSerializer
)
from .permissions import IsAdmin

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_student(request):
    serializer = StudentRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Student registered successfully',
            'user': UserSerializer(User.objects.get(username=serializer.validated_data['username'])).data
        }, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_teacher(request):
    serializer = TeacherRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Teacher registered successfully',
            'user': UserSerializer(User.objects.get(username=serializer.validated_data['username'])).data
        }, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    if not request.user.role == 'ADMIN':
        return Response({'detail': 'Forbidden'}, status=403)
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
