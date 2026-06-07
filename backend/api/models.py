from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    display_name = models.CharField(max_length=50, blank=True)
    avatar_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.display_name if self.display_name else self.user.username
    
class Book(models.Model):
    external_id = models.CharField(max_length=255, unique=True, db_index=True)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    title = models.CharField(max_length=255)
    authors = models.TextField(help_text="Zarezom odvojena imena autora")
    description = models.TextField(blank=True, null=True)
    cover_url = models.URLField(max_length=500, blank=True, null=True)
    published_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class Shelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, relatives_name="shelves")
    name = models.CharField(max_length=100)
    is_system = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    books = models.ManyToManyField(Book, blank=True, related_name="shelves")

    class Meta:
        # Spriječavamo da korisnik ima dvije police s istim imenom.
        unique_together = ('user', 'name')
        verbose_name_plural = "Shelves"

    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    # Ocjene ćemo imati između 1 i 5
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # korisnik može ostaviti najviše jednu recenziju za jednu knjigu
        unique_together = ('user', 'book')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} -> {self.book.title} ({self.rating}/5)"
