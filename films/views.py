from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import FilmListSerializer, FilmDetailSerializer


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
        film.title = request.data.get('title')
        film.text = request.data.get('text')
        film.rating = request.data.get('rating')
        film.is_hit = request.data.get('is_hit')
        film.release_year = request.data.get('release_year')
        film.director_id = request.data.get('director_id')
        film.genres.set(request.data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def film_list_create_api_view(request):
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
        title = request.data.get('title')
        description = request.data.get('text')
        release_year = request.data.get('release_year')
        rating = request.data.get('rating')
        is_hit = request.data.get('is_hit')
        director_id = request.data.get('director_id')
        genres = request.data.get('genres')

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
