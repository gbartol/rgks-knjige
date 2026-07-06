from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile, Book, Shelf, Review, Follow


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
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'avatar_url', 'is_following']

    def get_is_following(self, obj):
        # Prati li prijavljeni korisnik ovog korisnika. obj je Profile (pretraga)
        # ili User (kad se serializer koristi ugniježđeno) — pokrivamo oba.
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        target_user = obj.user if hasattr(obj, 'user') else obj
        return Follow.objects.filter(follower=request.user, following=target_user).exists()

class BookSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'cover_url']

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'external_id', 'isbn', 'title', 'authors', 'description', 'cover_url', 'published_year']

class ReviewSerializer(serializers.ModelSerializer):

    # Review.user je User; UserSummarySerializer očekuje Profile, pa prosljeđujemo user.profile.
    user = UserSummarySerializer(source='user.profile', read_only=True)
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
