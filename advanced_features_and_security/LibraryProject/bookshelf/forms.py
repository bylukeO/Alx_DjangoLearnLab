"""
Forms for the bookshelf application.
Includes secure form implementations with input validation and XSS protection.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import escape
import bleach
import re
from .models import Book


class BookForm(forms.ModelForm):
    """
    Secure form for creating and editing books with input validation.
    Implements XSS protection through input sanitization and validation.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1000, 'max': 2030}),
        }
    
    def clean_title(self):
        """
        Validate and sanitize book title to prevent XSS attacks.
        """
        title = self.cleaned_data.get('title')
        if title:
            # Remove any HTML tags and sanitize input
            title = bleach.clean(title.strip(), tags=[], strip=True)
            
            # Validate title length and content
            if len(title) < 1:
                raise ValidationError("Title cannot be empty.")
            if len(title) > 200:
                raise ValidationError("Title cannot exceed 200 characters.")
            
            # Check for potentially malicious patterns
            if re.search(r'<script|javascript:|data:', title, re.IGNORECASE):
                raise ValidationError("Invalid characters in title.")
                
        return title
    
    def clean_author(self):
        """
        Validate and sanitize author name to prevent XSS attacks.
        """
        author = self.cleaned_data.get('author')
        if author:
            # Remove any HTML tags and sanitize input
            author = bleach.clean(author.strip(), tags=[], strip=True)
            
            # Validate author length and content
            if len(author) < 1:
                raise ValidationError("Author name cannot be empty.")
            if len(author) > 100:
                raise ValidationError("Author name cannot exceed 100 characters.")
            
            # Check for potentially malicious patterns
            if re.search(r'<script|javascript:|data:', author, re.IGNORECASE):
                raise ValidationError("Invalid characters in author name.")
                
        return author
    
    def clean_publication_year(self):
        """
        Validate publication year to ensure reasonable values.
        """
        year = self.cleaned_data.get('publication_year')
        if year is not None:
            current_year = 2030  # Allow some future publications
            if year < 1000 or year > current_year:
                raise ValidationError(f"Publication year must be between 1000 and {current_year}.")
        return year


class ExampleForm(forms.Form):
    """
    Example form demonstrating secure form handling practices.
    Includes CSRF protection and input validation.
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'maxlength': 100
        }),
        help_text="Your full name (max 100 characters)"
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }),
        help_text="A valid email address"
    )
    
    message = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message',
            'maxlength': 500
        }),
        help_text="Your message (max 500 characters)"
    )
    
    def clean_name(self):
        """
        Validate and sanitize name input to prevent XSS attacks.
        """
        name = self.cleaned_data.get('name')
        if name:
            # Remove any HTML tags and sanitize input
            name = bleach.clean(name.strip(), tags=[], strip=True)
            
            # Validate name length and content
            if len(name) < 1:
                raise ValidationError("Name cannot be empty.")
            if len(name) > 100:
                raise ValidationError("Name cannot exceed 100 characters.")
            
            # Check for potentially malicious patterns
            if re.search(r'<script|javascript:|data:|on\w+\s*=', name, re.IGNORECASE):
                raise ValidationError("Invalid characters in name.")
                
        return name
    
    def clean_message(self):
        """
        Validate and sanitize message input to prevent XSS attacks.
        """
        message = self.cleaned_data.get('message')
        if message:
            # Remove any HTML tags and sanitize input
            message = bleach.clean(message.strip(), tags=[], strip=True)
            
            # Validate message length and content
            if len(message) < 1:
                raise ValidationError("Message cannot be empty.")
            if len(message) > 500:
                raise ValidationError("Message cannot exceed 500 characters.")
            
            # Check for potentially malicious patterns
            if re.search(r'<script|javascript:|data:|on\w+\s*=', message, re.IGNORECASE):
                raise ValidationError("Invalid characters in message.")
                
        return message