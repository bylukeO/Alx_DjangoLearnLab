# Retrieve the created Book instance in the Django shell

```python
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
# 1984 George Orwell 1949
```

# The Book instance was successfully retrieved and its attributes displayed. 