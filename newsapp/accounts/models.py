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
    user_saved_news = models.ManyToManyField(News, blank=True, related_name='likes')
    user_last_news = models.ManyToManyField(News, blank=True, related_name='last_news')
    user_news_historic = models.ManyToManyField(News, blank=True, related_name='historic')
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

    def get_interests(self):
        return list(self.interests.all())

    def add_interest(self, news_item):
        self.interests.add(news_item)

    def remove_interest(self, news_item):
        self.interests.remove(news_item)

    def get_saved_news(self):
        return list(self.user_saved_news.all())
    
    def add_saved_news(self, news_item):
        self.user_saved_news.add(news_item)
    
    def add_to_historic(self, news_item):
        self.user_news_historic.add(news_item)
        
