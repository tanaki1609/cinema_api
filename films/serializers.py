from rest_framework import serializers
from .models import Film, Director, Genre
from rest_framework.exceptions import ValidationError


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class DirectorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id fio birthday'.split()


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id fio'.split()


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmListSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = ['id', 'title', 'rating', 'release_year', 'director', 'genres', 'reviews']
        depth = 1

    def get_genres(self, film):
        return film.genre_list()


class FilmValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=255)
    text = serializers.CharField(required=False)
    release_year = serializers.IntegerField()
    rating = serializers.FloatField(min_value=0, max_value=10)
    is_hit = serializers.BooleanField(default=False)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist!')
        return director_id
