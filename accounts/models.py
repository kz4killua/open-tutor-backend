from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password):
        """Create a user with an email and a password."""

        # Make sure an email is supplied
        if not email:
            raise ValueError("Users must have an email address.")

        # Create the user
        user = self.model(email=email.lower())
        user.set_password(password)

        # Save and return the user
        user.save()
        return user


    def create_superuser(self, email, password):
        """Create a superuser with an email and password."""

        # Create a regular user
        user = self.create_user(email, password)

        # Apply superuser privileges
        user.is_superuser = True
        user.is_staff = True

        # Save and return the user
        user.save()
        return user
    

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self) -> str:
        return self.email