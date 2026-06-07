from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Profile
from .serializers import ProfileSerializer, UserSummarySerializer


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
