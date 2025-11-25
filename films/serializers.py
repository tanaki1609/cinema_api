from rest_framework import serializers
from .models import Film


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'rating', 'release_year']
        # fields = 'id title rating release_year'.split()
        # fields = '__all__'
        # exclude = ['id', 'updated']
