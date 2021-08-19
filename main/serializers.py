from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from account.models import CustomUser
from .models import *
from decimal import Decimal

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
        fields = ("name", "text", "replies", 'movie')


class MovieListSerializer(ModelSerializer):
    # СПИСОК ФИЛЬМОВ
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')

        # def to_representation(self, instance):
        #     representation = super().to_representation(instance)
        #     action = self.context.get('action')
        #     if action == 'list' or action == 'retrieve':
        #         likes = Like.objects.filter(movie=instance)
        #         if not likes:
        #             representation['likes'] = 'null'
        #         else:
        #             representation['likes'] = likes.count()
        #     return representation

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.like.count()
        rates = Rating.objects.filter(movie=instance)
        if not rates:
            representation['rating'] = 'null'
        else:
            sum = 0
            for i in rates:
                sum = sum + i.value
            representation['rating'] = Decimal(sum) / Decimal(Rating.objects.filter(movie=instance).count())

        return representation


class MovieDetailSerializer(ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
         model = Movie
         exclude = ('draft',)


class MovieCreateSerializer(ModelSerializer):
    # для создание фильмов

    class Meta:
        model = Movie
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("user", "value", "movie")

    def create(self, validated_data):
        request = self.context.get('request')
        rating, obj = Rating.objects.update_or_create(user__email=request.user.email, **validated_data)
        return rating

class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        likes, obj = Like.objects.update_or_create(user__email=request.user.email, **validated_data)
        return likes

