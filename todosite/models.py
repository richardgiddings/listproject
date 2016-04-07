from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    """
    Manage the creation of users
    """
    def _create_user(self, email, password, is_staff, is_superuser, 
                     **extra_fields):

        user = self.model(
                          email = self.normalize_email(email),
                          timezone = timezone,
                          known_as = known_as,
                          is_staff=is_staff, 
                          is_active=True,
                          is_superuser=is_superuser,
                          **extra_fields
                         )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):

        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        return self._create_user(email, password, True, True, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    A class representing a user of the application
    """
    email = models.EmailField(unique=True)
    timezone = models.CharField(max_length=255)
    known_as = models.CharField(max_length=20, 
                                help_text="Maximum of 20 characters.")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['timezone', 'known_as',]

    objects = CustomUserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

class Task(models.Model):
    """
    A class representing a task to do.
    """
 
    task_title = models.CharField(max_length=20,
                                  help_text="Maximum of 20 characters.")

    task_description = models.TextField(max_length=300,
                       help_text="Maximum of 300 characters.")

    task_due = models.DateTimeField('Date due', 
                                    default=timezone.now)

    belongs_to = models.ForeignKey(UserProfile)

    def __str__(self):
        return self.task_title
