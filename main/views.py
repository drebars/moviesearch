from django.shortcuts import render

import rest_framework.generics as generics
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from main.models import Movie, Actor
from main.serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, ActorListSerializer, \
    ActorDetailSerializer, CreateRatingSerializer, MovieCreateSerializer


class MovieCreateView(generics.CreateAPIView):
    queryset = Movie
    serializer_class = MovieCreateSerializer



class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    # filter_backends = (DjangoFilterBackend, )
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_fields = ['category']
    search_fields = ['title', 'year']


class MovieView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer



# class MovieDetailView(generics.RetrieveAPIView):
#     # ВЫВОД самого фильма
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer

class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(APIView):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=self.get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)

class ActorsListView(generics.ListAPIView):
    """Вывод списка актеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsView(generics.RetrieveUpdateDestroyAPIView):
    """Вывод актера"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer