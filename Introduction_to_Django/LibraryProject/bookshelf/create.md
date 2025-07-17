# Create a Book instance in the Django shell

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# <Book: 1984 by George Orwell (1949)>
```

# The Book instance was successfully created with the specified attributes. 