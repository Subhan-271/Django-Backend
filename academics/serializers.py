from rest_framework import serializers
from .models import Program, Course, PLO, CLO

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class PLOSerializer(serializers.ModelSerializer):
    class Meta:
        model = PLO
        fields = '__all__'

class CLOSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLO
        fields = '__all__'
