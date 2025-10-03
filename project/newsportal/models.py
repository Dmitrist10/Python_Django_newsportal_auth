from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class RatingSystem(models.Model):
    rating = models.FloatField(default=0)

    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def recalculate_rating(self):
        total_votes = self.likes + self.dislikes

        if total_votes > 0:
            self.rating = round((self.likes / total_votes) * 5, 1)
        else:
            self.rating = 0.0
        self.save()

    def like(self):
        self.likes += 1
        self.recalculate_rating()

    def dislike(self):
        self.dislikes += 1
        self.recalculate_rating()

    class Meta:
        abstract = True


class Author(RatingSystem, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Author_Account_creation_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f"Category: {self.name}"


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=15000)

    creation_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey("Author", on_delete=models.CASCADE, blank=True, null=True)

class Article(Post, RatingSystem):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f"Articles: {self.title} by {self.author}"
    
    def get_absolute_url(self):
        return reverse('Article_Detail', args=[str(self.pk)])


class News(Post, RatingSystem):

    def __str__(self) -> str:
        return f"News: {self.title} by {self.author}"
    
    def get_absolute_url(self):
        return reverse('New_Detail', args=[str(self.pk)])