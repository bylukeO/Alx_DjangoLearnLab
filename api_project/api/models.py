from django.db import models

# Create your models here.

class Book(models.Model):
    """
    Simple Book model for API demonstration.
    Contains basic information about books.
    """
    title = models.CharField(max_length=200, help_text="Title of the book")
    author = models.CharField(max_length=100, help_text="Author of the book")
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    class Meta:
        ordering = ['title']
        verbose_name = "Book"
        verbose_name_plural = "Books"
