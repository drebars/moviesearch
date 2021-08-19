from django.urls import path

from .views import  ReviewCreateView

urlpatterns = [
    path('review/', ReviewCreateView.as_view()),
]