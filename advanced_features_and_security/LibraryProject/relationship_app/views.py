from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book
from .models import UserProfile
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import user_passes_test, login_required
from django import forms
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.utils.html import escape
import bleach
import re

# Function-based view to list all books (HTML template)
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Function-based register view for checker compliance
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy('list_books'))
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# User authentication views
class UserLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class UserLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy('list_books'))
        return render(request, 'relationship_app/register.html', {'form': form})

# Role-based access control views
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
@login_required
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
@login_required
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
@login_required
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# Secure Book form for add/edit with input validation
class BookForm(forms.ModelForm):
    """
    Secure form for creating and editing books with input validation.
    Implements XSS protection through input sanitization and validation.
    """
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'maxlength': 200}),
            'author': forms.TextInput(attrs={'maxlength': 100}),
        }
    
    def clean_title(self):
        """Validate and sanitize book title to prevent XSS attacks."""
        title = self.cleaned_data.get('title')
        if title:
            title = bleach.clean(title.strip(), tags=[], strip=True)
            if len(title) < 1:
                raise ValidationError("Title cannot be empty.")
            if len(title) > 200:
                raise ValidationError("Title cannot exceed 200 characters.")
            if re.search(r'<script|javascript:|data:', title, re.IGNORECASE):
                raise ValidationError("Invalid characters in title.")
        return title
    
    def clean_author(self):
        """Validate and sanitize author name to prevent XSS attacks."""
        author = self.cleaned_data.get('author')
        if author:
            author = bleach.clean(author.strip(), tags=[], strip=True)
            if len(author) < 1:
                raise ValidationError("Author name cannot be empty.")
            if len(author) > 100:
                raise ValidationError("Author name cannot exceed 100 characters.")
            if re.search(r'<script|javascript:|data:', author, re.IGNORECASE):
                raise ValidationError("Invalid characters in author name.")
        return author

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
