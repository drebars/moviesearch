from django.urls import path

from .views import MovieListView, ReviewCreateView, ActorsListView, AddStarRatingView, MovieCreateView, ActorsView, MovieView

urlpatterns = [
    path('movie/', MovieListView.as_view()),
    path('review/', ReviewCreateView.as_view()),
    path('actors/', ActorsListView.as_view()),
    path('actors/<int:pk>/', ActorsView.as_view()),
    path('rating/', AddStarRatingView.as_view()),
    path('create-movie/', MovieCreateView.as_view()),
    path('movie/<int:pk>/', MovieView.as_view()),
]