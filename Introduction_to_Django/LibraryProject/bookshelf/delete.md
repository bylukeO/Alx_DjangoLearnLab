# Delete the Book instance in the Django shell and confirm deletion

```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
# <QuerySet []>
```

# The Book instance was successfully deleted and no books remain in the database. 