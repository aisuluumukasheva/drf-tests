from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True


    def create_user(self,email,password,**kwargs):
        assert email, 'Email is required'
        email = self.normalize_email(email)
        user:User = self.model(email=email, **kwargs) # создаем объект от юзера и передаем поля
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self,email,password,**kwargs):
        assert email, 'Email is required'
        email = self.normalize_email(email)
        kwargs['is_staff'] = True
        kwargs['is_active'] = True
        kwargs['is_superuser'] = True
        user:User = self.model(email=email, **kwargs) # создаем объект от юзера и передаем поля
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = UserManager()