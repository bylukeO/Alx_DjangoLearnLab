# Update the title of the Book instance in the Django shell

```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
# Nineteen Eighty-Four
```

# The Book instance's title was successfully updated. 