from django.contrib import admin
from .models import Article, News, Author, Category

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)

admin.site.register(News)
admin.site.register(Article)