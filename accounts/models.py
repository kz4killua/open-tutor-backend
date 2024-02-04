from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, password):
        """Creates a user with a username and a password."""

        # Make sure a username is supplied
        if not username:
            raise ValueError("Users must have a username.")
        
        # Create the user
        user = self.model(username=username)
        user.set_password(password)

        # Save and return the user
        user.save()
        return user
    

    def create_superuser(self, username, email, password):
        """Create a superuser with a username and password."""

        # Create a regular user
        user = self.create_user(username, password)

        # Apply superuser privileges
        user.is_superuser = True
        user.is_staff = True

        # Save and return the user
        user.save()
        return user


class User(AbstractUser):
    objects = UserManager()

    def __str__(self):
        return self.username