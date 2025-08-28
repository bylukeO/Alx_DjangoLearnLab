from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """Form for creating and editing books."""
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }


@permission_required('bookshelf.can_view', raise_exception=True)
@login_required
def book_list(request):
    """Display list of all books - requires can_view permission."""
    books = Book.objects.all()
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
    """Create a new book - requires can_create permission."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
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
