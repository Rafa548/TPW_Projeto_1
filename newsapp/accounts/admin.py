from django.contrib import admin

from .models import User, Interest
from reader.models import News

admin.site.register(User)
admin.site.register(Interest)
admin.site.register(News)