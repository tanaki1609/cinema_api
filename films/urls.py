from django.urls import path
from . import views
from .constants import L_C, R_U_D

urlpatterns = [
    path('', views.film_list_api_view),
    path('<int:id>/', views.film_detail_api_view),
    path('genres/', views.GenreListAPIView.as_view()),
    path('genres/<int:id>/', views.GenreDetailAPIView.as_view()),
    path('directors/', views.DirectorViewSet.as_view(L_C)),
    path('directors/<int:id>/', views.DirectorViewSet.as_view(R_U_D))
]
