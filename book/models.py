from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200, null=True, default=None, blank=True)
    authors = models.ManyToManyField(Author, related_name='books')
    description = models.CharField(max_length=400, null=True, default=None, blank=True)
    cover_image = models.ImageField(upload_to="static/cover_image/", default=None, null=True, blank=True)
    ratings = models.SmallIntegerField()
    google_book_id = models.CharField(max_length=50)
    liked_by = models.ManyToManyField(User, related_name='likes', )
    recommended_by = models.ManyToManyField(User, related_name='recommendations', )
    publication_date = models.CharField(max_length=50, null=True, default=None, blank=True) # not making this date field as data can have only year otherwise would have converted to date and then saved
    genres = models.ManyToManyField(Genre, related_name='books')

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} commented on {self.book.title}"
