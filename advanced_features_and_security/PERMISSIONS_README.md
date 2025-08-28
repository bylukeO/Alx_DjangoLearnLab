# Django Permissions and Groups System

This document explains the permissions and groups system implemented in the LibraryProject to control access to various parts of the application.

## Overview

The system implements role-based access control (RBAC) using Django's built-in permissions and groups functionality. Users are assigned to groups, and groups are granted specific permissions to perform actions on Book objects.

## Custom Permissions

The following custom permissions have been defined for the Book model in `bookshelf/models.py`:

- `can_view`: Allows users to view book details and list books
- `can_create`: Allows users to create new books
- `can_edit`: Allows users to edit existing books
- `can_delete`: Allows users to delete books

## User Groups

Three user groups have been created with different permission levels:

### 1. Viewers Group
- **Permissions**: `can_view`
- **Capabilities**: Can only view books and book details
- **Cannot**: Create, edit, or delete books

### 2. Editors Group
- **Permissions**: `can_view`, `can_create`, `can_edit`
- **Capabilities**: Can view, create, and edit books
- **Cannot**: Delete books

### 3. Admins Group
- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **Capabilities**: Full access to all book operations
- **Can**: Perform all CRUD operations on books

## Implementation Details

### Models (bookshelf/models.py)
```python
class Book(models.Model):
    # ... model fields ...
    
    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
```

### Views with Permission Enforcement (bookshelf/views.py)
All views are protected using Django's `@permission_required` decorator:

```python
@permission_required('bookshelf.can_view', raise_exception=True)
@login_required
def book_list(request):
    # View implementation

@permission_required('bookshelf.can_create', raise_exception=True)
@login_required
def book_create(request):
    # Create implementation

@permission_required('bookshelf.can_edit', raise_exception=True)
@login_required
def book_edit(request, pk):
    # Edit implementation

@permission_required('bookshelf.can_delete', raise_exception=True)
@login_required
def book_delete(request, pk):
    # Delete implementation
```

### Template Permission Checks
Templates use Django's permission checking to conditionally display actions:

```html
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}" class="btn btn-primary">Add Book</a>
{% endif %}

{% if perms.bookshelf.can_edit %}
    <a href="{% url 'book_edit' book.pk %}" class="btn btn-warning">Edit</a>
{% endif %}

{% if perms.bookshelf.can_delete %}
    <a href="{% url 'book_delete' book.pk %}" class="btn btn-danger">Delete</a>
{% endif %}
```

## Setup Instructions

### 1. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Groups and Assign Permissions
```bash
python manage.py setup_groups
```

### 3. Create Test Users (Optional)
```bash
python manage.py create_test_users
```

### 4. Create Sample Books (Optional)
```bash
python manage.py create_sample_books
```

## Testing the Permission System

### Test Users
Three test users have been created for testing different permission levels:

- **viewer@test.com** / testpass123 (Viewers group)
- **editor@test.com** / testpass123 (Editors group)
- **admin@test.com** / testpass123 (Admins group)

### Manual Testing Steps

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the bookshelf application**:
   Navigate to `http://127.0.0.1:8000/bookshelf/`

3. **Test different user permissions**:
   - Login as `viewer@test.com`: Can only view books
   - Login as `editor@test.com`: Can view, create, and edit books
   - Login as `admin@test.com`: Can perform all operations

4. **Verify permission enforcement**:
   - Try accessing URLs directly without proper permissions
   - Check that UI elements (buttons, links) are conditionally displayed
   - Verify that unauthorized actions result in permission denied errors

## Security Features

### Permission Decorators
- All views require authentication (`@login_required`)
- Specific permissions are enforced using `@permission_required` with `raise_exception=True`
- Unauthorized access results in HTTP 403 Forbidden responses

### Template Security
- UI elements are conditionally displayed based on user permissions
- Users only see actions they're authorized to perform
- Permission status is clearly displayed to users

### Admin Integration
- Custom admin configuration respects the permission system
- Book admin access requires appropriate permissions
- User groups and permissions can be managed through Django admin

## File Structure

```
bookshelf/
├── models.py                    # Book model with custom permissions
├── views.py                     # Views with permission enforcement
├── admin.py                     # Admin configuration with permissions
├── urls.py                      # URL configuration
├── templates/bookshelf/         # Templates with permission checks
│   ├── base.html
│   ├── book_list.html
│   ├── book_detail.html
│   ├── book_form.html
│   └── book_confirm_delete.html
└── management/commands/         # Management commands
    ├── setup_groups.py          # Creates groups and assigns permissions
    ├── create_test_users.py     # Creates test users
    └── create_sample_books.py   # Creates sample data
```

## Key Features

1. **Role-Based Access Control**: Users assigned to groups with specific permissions
2. **Permission Enforcement**: View-level and template-level permission checks
3. **User-Friendly**: Clear indication of user permissions and available actions
4. **Secure**: All sensitive operations require appropriate permissions
5. **Flexible**: Easy to extend with additional permissions and groups
6. **Testable**: Includes test users and sample data for validation

## Troubleshooting

### Common Issues

1. **Permission Denied Errors**: Ensure user is in the correct group with required permissions
2. **Missing Groups**: Run `python manage.py setup_groups` to create groups
3. **Template Errors**: Check that user is authenticated when checking permissions
4. **Database Issues**: Ensure migrations are applied after adding permissions

### Verification Commands

```bash
# Check user groups and permissions
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(email='viewer@test.com')
>>> user.groups.all()
>>> user.get_all_permissions()
```

This permissions and groups system provides a robust foundation for controlling access to your Django application while maintaining security and user experience.