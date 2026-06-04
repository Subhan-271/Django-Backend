from django.contrib import admin
from .models import User


class AuditAdminMixin(admin.ModelAdmin):
    """
    Reusable admin mixin for created_by / updated_by
    """
    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by") and not obj.pk:
            obj.created_by = request.user
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(User)
class UserAdmin(AuditAdminMixin):
    list_display = ('id', 'username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')
