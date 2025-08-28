from django.core.management.base import BaseCommand
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Create sample books for testing permissions'

    def handle(self, *args, **options):
        sample_books = [
            {
                'title': 'Django Security Best Practices',
                'author': 'Security Expert',
                'publication_year': 2023
            },
            {
                'title': 'Python Web Development',
                'author': 'Code Master',
                'publication_year': 2022
            },
            {
                'title': 'User Authentication Systems',
                'author': 'Auth Specialist',
                'publication_year': 2024
            },
            {
                'title': 'Database Design Patterns',
                'author': 'DB Architect',
                'publication_year': 2021
            },
        ]

        created_count = 0
        for book_data in sample_books:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created book: {book.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Book already exists: {book.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nCreated {created_count} new books. Total books: {Book.objects.count()}')
        )