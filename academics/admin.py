from django.contrib import admin
from .models import Program, Course, PLO, CLO


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'created_at')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'course_class',
        'credit_hours_theory',
        'credit_hours_lab',
        'created_at',
    )
    filter_horizontal = ('pre_requisites', 'co_requisites')


@admin.register(PLO)
class PLOAdmin(admin.ModelAdmin):
    list_display = ('program', 'created_at')


@admin.register(CLO)
class CLOAdmin(admin.ModelAdmin):
    list_display = ('course', 'created_at')
