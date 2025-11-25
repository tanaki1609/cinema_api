from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import FilmListSerializer, FilmDetailSerializer


@api_view(['GET'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)  # DoesNotExist / MultiKeyError
    except Film.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Film not found!'})
    item = FilmDetailSerializer(film, many=False).data
    return Response(data=item, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def film_list_api_view(request):
    # step 1: Collect films from DB (QuerySet)
    films = Film.objects.all()

    # step 2: Reformat QuerySet to list of dictionaries (Serializer)
    list_ = FilmListSerializer(films, many=True).data

    # step 3: Return Response
    return Response(
        data=list_,  # dict, list (int, str, bool, dict)
        status=status.HTTP_200_OK,  # int (100, 200, 300, 400, 500)
    )
