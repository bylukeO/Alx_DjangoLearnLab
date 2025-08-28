from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users and assign them to different groups'

    def handle(self, *args, **options):
        # Get the groups
        try:
            viewers_group = Group.objects.get(name='Viewers')
            editors_group = Group.objects.get(name='Editors')
            admins_group = Group.objects.get(name='Admins')
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Groups not found. Please run setup_groups command first.')
            )
            return

        # Create test users
        test_users = [
            {
                'email': 'viewer@test.com',
                'password': 'testpass123',
                'first_name': 'Test',
                'last_name': 'Viewer',
                'group': viewers_group
            },
            {
                'email': 'editor@test.com',
                'password': 'testpass123',
                'first_name': 'Test',
                'last_name': 'Editor',
                'group': editors_group
            },
            {
                'email': 'admin@test.com',
                'password': 'testpass123',
                'first_name': 'Test',
                'last_name': 'Admin',
                'group': admins_group
            },
        ]

        for user_data in test_users:
            email = user_data['email']
            group = user_data.pop('group')
            
            # Create or get user
            user, created = User.objects.get_or_create(
                email=email,
                defaults=user_data
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {email}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User {email} already exists')
                )
            
            # Add user to group
            if group not in user.groups.all():
                user.groups.add(group)
                self.stdout.write(
                    self.style.SUCCESS(f'Added {email} to {group.name} group')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'{email} is already in {group.name} group')
                )

        self.stdout.write(
            self.style.SUCCESS('\nTest users created successfully!')
        )
        self.stdout.write('Login credentials:')
        self.stdout.write('  viewer@test.com / testpass123 (Viewers group)')
        self.stdout.write('  editor@test.com / testpass123 (Editors group)')
        self.stdout.write('  admin@test.com / testpass123 (Admins group)')