# Django Admin Integration for Book Model

## 1. Register the Book Model with the Admin

To enable admin functionalities for the Book model, we register it in `bookshelf/admin.py`:

```python
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    list_filter = ("author", "publication_year")
    search_fields = ("title", "author")
```

## 2. Customize the Admin Interface

- **list_display**: Shows the `title`, `author`, and `publication_year` columns in the admin list view for books.
- **list_filter**: Adds sidebar filters for `author` and `publication_year`, making it easy to filter books by these fields.
- **search_fields**: Enables a search box that allows admin users to search books by `title` or `author`.

## 3. How to Use

1. Run the development server:
   ```bash
   python manage.py runserver
   ```
2. Log in to the admin panel at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
3. You will see the Book model listed. You can now:
   - View all books with the specified columns
   - Filter books by author or publication year
   - Search for books by title or author

## 4. Benefits

- **Improved visibility**: Key book details are visible at a glance.
- **Efficient management**: Filters and search make it easy to find and manage books, even in large collections.

---

*This setup ensures a user-friendly and powerful admin interface for managing your library's books.* 