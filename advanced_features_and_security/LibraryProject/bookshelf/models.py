from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Custom user manager that handles user creation with additional fields."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser with additional fields."""
    
    # Remove username field and use email as primary identifier
    username = None
    email = models.EmailField('Email Address', unique=True)
    
    # Additional custom fields
    date_of_birth = models.DateField('Date of Birth', null=True, blank=True)
    profile_photo = models.FileField('Profile Photo', upload_to='profile_photos/', null=True, blank=True)
    
    # Use email as the unique identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # Attach the custom manager
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        permissions = [
            ("can_view_user", "Can view user"),
            ("can_edit_user", "Can edit user"),
        ]
    
    def __str__(self):
        return f"{self.email} ({self.get_full_name()})"
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    @property
    def age(self):
        """Calculate and return the user's age based on date_of_birth."""
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
