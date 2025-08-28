from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **options):
        # Get the Book content type
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get or create permissions
        can_view, created = Permission.objects.get_or_create(
            codename='can_view',
            name='Can view book',
            content_type=book_content_type,
        )
        can_create, created = Permission.objects.get_or_create(
            codename='can_create',
            name='Can create book',
            content_type=book_content_type,
        )
        can_edit, created = Permission.objects.get_or_create(
            codename='can_edit',
            name='Can edit book',
            content_type=book_content_type,
        )
        can_delete, created = Permission.objects.get_or_create(
            codename='can_delete',
            name='Can delete book',
            content_type=book_content_type,
        )

        # Create groups and assign permissions
        
        # Viewers group - can only view books
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        viewers_group.permissions.set([can_view])
        if created:
            self.stdout.write(self.style.SUCCESS('Created Viewers group'))
        else:
            self.stdout.write(self.style.WARNING('Viewers group already exists, updated permissions'))

        # Editors group - can view, create, and edit books
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editors_group.permissions.set([can_view, can_create, can_edit])
        if created:
            self.stdout.write(self.style.SUCCESS('Created Editors group'))
        else:
            self.stdout.write(self.style.WARNING('Editors group already exists, updated permissions'))

        # Admins group - can perform all actions on books
        admins_group, created = Group.objects.get_or_create(name='Admins')
        admins_group.permissions.set([can_view, can_create, can_edit, can_delete])
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admins group'))
        else:
            self.stdout.write(self.style.WARNING('Admins group already exists, updated permissions'))

        self.stdout.write(
            self.style.SUCCESS('Successfully configured groups and permissions:')
        )
        self.stdout.write('  - Viewers: can_view')
        self.stdout.write('  - Editors: can_view, can_create, can_edit')
        self.stdout.write('  - Admins: can_view, can_create, can_edit, can_delete')