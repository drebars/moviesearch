from django.shortcuts import render
from collections import OrderedDict
import rest_framework.generics as generics
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

# from .permissions import IsAdminUserOrReadOnly
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from main.models import *
from main.serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, ActorListSerializer, \
    ActorDetailSerializer,  MovieCreateSerializer, RatingSerializer, LikeSerializer
from .service import MovieFilter




class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        else:
            return ActorDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]
        return [permission() for permission in self.permission_classes]



class MoviePagination(PageNumberPagination):

    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('objects_count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('movies', data)
        ]))


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MovieFilter
    search_fields = ['title']
    pagination_class = MoviePagination
    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        else:
            return MovieDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]
        return [permission() for permission in self.permission_classes]


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    # def get_serializer_class(self):
    #     context = super().get_serializer_context()
    #     context['action'] = self.action
    #     return context