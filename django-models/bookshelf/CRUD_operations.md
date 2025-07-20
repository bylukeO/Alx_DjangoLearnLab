# CRUD Operations with Django ORM

This document summarizes the Create, Retrieve, Update, and Delete operations performed using the Django shell.

---

##  Create a Book

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# <Book: 1984>


##  Retrieve the Book

book = Book.objects.get(title="1984")
book.title
# '1984'
book.author
# 'George Orwell'
book.publication_year
# 1949

## Update the Book

book.title = "Nineteen Eighty-Four"
book.save()
book.title
# 'Nineteen Eighty-Four'

## Delete the Book

book.delete()
# (1, {'bookshelf.Book': 1})

Book.objects.all()
# <QuerySet []>



