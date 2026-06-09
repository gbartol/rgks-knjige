from django.urls import path

from . import views


urlpatterns = [
    # Ovdje dodajemo url-ove kada napravimo neku rutu
    path('profile/me/', views.my_profile, name='my-profile'),
    path('users/', views.user_search, name='user-search'),
    path('books/search/', views.book_search, name='book-search'),
    path('books/<str:external_id>/', views.book_detail, name='book-detail'),
    path('books/<str:external_id>/reviews/', views.add_review, name='add-review'),
    path('shelves/', views.shelf_list_create, name='shelf-list-create'),
    path('shelves/<int:shelf_id>/<str:action>/', views.modify_shelf_books, name='modify-shelf-books')
]
