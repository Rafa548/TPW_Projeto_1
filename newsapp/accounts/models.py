from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager
from reader.models import News


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    interests = models.ManyToManyField(Interest, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    likes = models.ManyToManyField(News, blank=True, related_name='likes')
    # set a manager role for shop manager to access orders and products
    is_manager = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_likes_count(self):
        return self.likes.count()

    def get_interests(self):
        return list(self.interests.all())

    def add_interest(self, news_item):
        self.interests.add(news_item)

    def remove_interest(self, news_item):
        self.interests.remove(news_item)