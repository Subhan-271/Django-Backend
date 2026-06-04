from django.contrib import admin
from .models import Assessment, Question


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'total_marks')
    search_fields = ('title',)
    list_filter = ('course',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'assessment', 'marks')
    list_filter = ('assessment',)
