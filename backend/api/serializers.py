from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile, Book, Shelf, Review


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['display_name', 'avatar_url']
        read_only_fields = ['user']


class UserSummarySerializer(serializers.ModelSerializer):
    # Prikaz korisnika (rezultati pretrage, autor recenzije...).
    # Baziran na Profile-u: display_name/avatar_url su njegova polja, a id/username
    # dolaze s povezanog User-a.
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'avatar_url']

class BookSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'cover_url']

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'external_id', 'isbn', 'title', 'authors', 'description', 'cover_url', 'published_year']

class ReviewSerializer(serializers.ModelSerializer):
    
    user = UserSummarySerializer(read_only=True)
    book = BookSummarySerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'text', 'created_at']
        read_only_fields = ['created_at']

class ShelfSerializer(serializers.ModelSerializer):

    books_count = serializers.IntegerField(source='books.count', read_only=True)

    class Meta:
        model = Shelf
        fields = ['id', 'name', 'is_system', 'is_public', 'books_count']
        read_only_fields = ['is_system']
