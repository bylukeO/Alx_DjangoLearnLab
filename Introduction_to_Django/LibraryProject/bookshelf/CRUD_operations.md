# CRUD Operations for Book Model

## Create
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# <Book: 1984 by George Orwell (1949)>
```
# The Book instance was successfully created with the specified attributes.

---

## Retrieve
```python
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
# 1984 George Orwell 1949
```
# The Book instance was successfully retrieved and its attributes displayed.

---

## Update
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
# Nineteen Eighty-Four
```
# The Book instance's title was successfully updated.

---

## Delete
```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
# <QuerySet []>
```
# The Book instance was successfully deleted and no books remain in the database. 