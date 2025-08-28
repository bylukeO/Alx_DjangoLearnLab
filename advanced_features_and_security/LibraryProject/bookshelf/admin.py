from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Book, CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form for the admin interface."""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    """Custom user change form for the admin interface."""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo')


class CustomUserAdmin(UserAdmin):
    """Custom user admin configuration."""
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    # Fields to display in the admin list view
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    
    # Fields for searching users
    search_fields = ['email', 'first_name', 'last_name']
    
    # Ordering
    ordering = ['email']
    
    # Fieldsets for organizing the admin form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model with permissions info."""
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')
    
    def has_module_permission(self, request):
        """Allow access to the Book admin if user has any book permission."""
        return (
            request.user.has_perm('bookshelf.can_view') or
            request.user.has_perm('bookshelf.can_create') or
            request.user.has_perm('bookshelf.can_edit') or
            request.user.has_perm('bookshelf.can_delete') or
            super().has_module_permission(request)
        )


# Register the custom user model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
