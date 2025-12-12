from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film, Director, Genre
from .serializers import (FilmListSerializer,
                          FilmDetailSerializer,
                          FilmValidateSerializer,
                          DirectorSerializer,
                          GenreSerializer,
                          DirectorCreateSerializer)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class DirectorListCreateAPIView(ListCreateAPIView):
    queryset = Director.objects.all()  # list of data from DB
    serializer_class = DirectorSerializer  # serializer inherited by ModelSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DirectorCreateSerializer
        return self.serializer_class


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'


@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)  # DoesNotExist / MultiKeyError
    except Film.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Film not found!'})
    if request.method == 'GET':
        item = FilmDetailSerializer(film, many=False).data
        return Response(data=item, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = FilmValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        film.title = serializer.validated_data.get('title')
        film.text = serializer.validated_data.get('text')
        film.rating = serializer.validated_data.get('rating')
        film.is_hit = serializer.validated_data.get('is_hit')
        film.release_year = serializer.validated_data.get('release_year')
        film.director_id = serializer.validated_data.get('director_id')
        film.genres.set(serializer.validated_data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def film_list_create_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # step 1: Collect films from DB (QuerySet)
        films = Film.objects.select_related('director').prefetch_related('genres', 'reviews').all()

        # step 2: Reformat QuerySet to list of dictionaries (Serializer)
        list_ = FilmListSerializer(films, many=True).data

        # step 3: Return Response
        return Response(
            data=list_,  # dict, list (int, str, bool, dict)
            status=status.HTTP_200_OK,  # int (100, 200, 300, 400, 500)
        )
    elif request.method == 'POST':
        # Validation (Existing, Typing, Extra)
        print("Некорректные:", request.data)
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        print("Исправленные:", serializer.validated_data)

        title = serializer.validated_data.get('title')  # None
        description = serializer.validated_data.get('text')
        release_year = serializer.validated_data.get('release_year')
        rating = serializer.validated_data.get('rating')
        is_hit = serializer.validated_data.get('is_hit')  # "Y"
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')

        film = Film.objects.create(
            title=title,
            text=description,
            release_year=release_year,
            rating=rating,
            is_hit=is_hit,
            director_id=director_id,
        )
        film.genres.set(genres)
        film.save()

        return Response(status=status.HTTP_201_CREATED)
