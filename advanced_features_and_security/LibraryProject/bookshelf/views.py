from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils.html import escape
from .models import Book
from .forms import BookForm


@permission_required('bookshelf.can_view', raise_exception=True)
@login_required
def book_list(request):
    """
    Display list of all books - requires can_view permission.
    
    Security measures:
    - Uses Django ORM to prevent SQL injection attacks
    - Requires authentication and proper permissions
    - Safe context data passed to template
    """
    books = Book.objects.all()  # ORM query prevents SQL injection
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'user': request.user
    })


@permission_required('bookshelf.can_view', raise_exception=True)
@login_required
def book_detail(request, pk):
    """Display book details - requires can_view permission."""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {
        'book': book,
        'user': request.user
    })


@permission_required('bookshelf.can_create', raise_exception=True)
@login_required
def book_create(request):
    """
    Create a new book - requires can_create permission.
    
    Security measures:
    - CSRF protection through middleware and form token
    - Input validation and sanitization via BookForm
    - Permission-based access control
    - XSS prevention through form validation and template escaping
    """
    if request.method == 'POST':
        form = BookForm(request.POST)  # Form includes CSRF protection
        if form.is_valid():  # Validates and sanitizes all input
            book = form.save()
            # Escape output in success message to prevent XSS
            messages.success(request, f'Book "{escape(book.title)}" created successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'title': 'Create New Book',
        'user': request.user
    })


@permission_required('bookshelf.can_edit', raise_exception=True)
@login_required
def book_edit(request, pk):
    """Edit an existing book - requires can_edit permission."""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'title': f'Edit Book: {book.title}',
        'book': book,
        'user': request.user
    })


@permission_required('bookshelf.can_delete', raise_exception=True)
@login_required
def book_delete(request, pk):
    """Delete a book - requires can_delete permission."""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {
        'book': book,
        'user': request.user
    })
