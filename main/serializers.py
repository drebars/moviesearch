from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Movie, Actor, Review, Rating


class ActorListSerializer(ModelSerializer):
    # СПИСОК АКТЕРОВ И РЕЖИССЕРОВ

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')

class ActorDetailSerializer(ModelSerializer):
    # Детализация актера

    class Meta:
        model = Actor
        fields = '__all__'


class FilterReviewListSerializer(serializers.ListSerializer):
    """ Фильтрую комментарии чтобы высвечивались только родительские """
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивного комментария которого отв"""
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class ReviewCreateSerializer(ModelSerializer):
        # для создание комментов

        class Meta:
            model = Review
            fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    # VYVOD ОТЗЫВОВ в фильме
    replies = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "replies")


class MovieListSerializer(ModelSerializer):
    # СПИСОК ФИЛЬМОВ
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')


class MovieDetailSerializer(ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
         model = Movie
         exclude = ('draft',)

class CreateRatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(ip=validated_data.get('ip', None),
                                                 movie=validated_data.get('movie', None),
                                                 defaults={'star': validated_data.get('star')})
        return rating

class MovieCreateSerializer(ModelSerializer):
    # для создание фильмов

    class Meta:
        model = Movie
        fields = '__all__'
