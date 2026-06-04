from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    current_user,
    list_users,
    register_student,
    register_teacher
)

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/register/student/', register_student, name='register_student'),
    path('auth/register/teacher/', register_teacher, name='register_teacher'),
    path('me/', current_user, name='current_user'),
    path('users/', list_users, name='list_users'),
]
