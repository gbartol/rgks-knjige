from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Profile, Book, Shelf, Review
from .serializers import ProfileSerializer, UserSummarySerializer, BookSerializer, ShelfSerializer, ReviewSerializer
from .services import search_open_library, get_or_create_book


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ProfileSerializer(profile).data)

    elif request.method == 'PATCH':
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
def user_search(request):
    search = request.query_params.get('search', '').strip()
    profiles = (
        Profile.objects
        .select_related('user')
        .filter(display_name__icontains=search)
        .order_by('display_name')
    )
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(profiles, request)
    serializer = UserSummarySerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)

# PRETRAGA

@api_view(['GET'])
def book_search(request):
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response({"detail": "Morate unijeti pojam za pretragu."}, status=status.HTTP_400_BAD_REQUEST)
    
    results = search_open_library(query)
    return Response(results, status=status.HTTP_200_OK)

@api_view(['GET'])
def book_detail(request, external_id):
    try:
        book = get_or_create_book(external_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except ValueError as e:
        return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, external_id):
    book = get_or_create_book(external_id)
    
    if Review.objects.filter(user=request.user, book=book).exists():
        return Response({"detail": "Već ste recenzirali ovu knjigu."}, status=status.HTTP_400_BAD_REQUEST)
        
    serializer = ReviewSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user, book=book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def shelf_list_create(request):
    if request.method == 'GET':
        shelves = Shelf.objects.filter(user=request.user)
        serializer = ShelfSerializer(shelves, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = ShelfSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def modify_shelf_books(request, shelf_id, action):

    shelf = get_object_or_404(Shelf, id=shelf_id, user=request.user)
    external_id = request.data.get('external_id')
    
    if not external_id:
        return Response({"detail": "external_id je obavezan."}, status=status.HTTP_400_BAD_REQUEST)
        
    if action == 'add':
        book = get_or_create_book(external_id)
        shelf.books.add(book)
        return Response({"detail": f"Knjiga uspješno dodana na policu '{shelf.name}'."})
        
    elif action == 'remove':
        book = get_object_or_404(Book, external_id=external_id)
        shelf.books.remove(book)
        return Response({"detail": f"Knjiga uspješno maknuta s police '{shelf.name}'."})
        
    return Response({"detail": "Nepoznata akcija."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    """ DELETE /api/reviews/<review_id>/ """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)