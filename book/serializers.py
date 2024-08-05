from rest_framework import serializers
from book.models import Author, Book, Comment, Genre
from django.contrib.auth.models import User

from user.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    recommendations = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    can_remove_recommendations = serializers.SerializerMethodField()

    def get_authors(self, obj):
        return AuthorSerializer(obj.authors.all(), many=True).data

    def get_total_likes(self, obj):
        return obj.liked_by.count()
    
    def get_total_comments(self, obj):
        return Comment.objects.filter(book=obj).count()

    def get_genres(self, obj):
        return GenreSerializer(obj.genres.all(), many=True).data
    
    def get_recommendations(self, obj):
        return UserSerializer(obj.recommended_by.all(), many=True).data
    
    def get_can_remove_recommendations(self, obj):
        return obj.recommended_by.filter(id=self.context.get('user_id')).exists()
    
    def get_ratings(self, obj):
        if obj.ratings < 0:
            return None
        return obj.ratings

    class Meta:
        model = Book
        fields = ('title', 'authors', 'description', 'cover_image', 'can_remove_recommendations', 'ratings',
                   'google_book_id', 'total_likes', 'publication_date', 'genres', 'total_comments', 'recommendations', )

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name',)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
