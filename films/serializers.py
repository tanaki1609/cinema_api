from rest_framework import serializers
from .models import Film, Director


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
