from django.urls import path
from . import views

urlpatterns = [
    path('', views.film_list_api_view),
    path('<int:id>/', views.film_detail_api_view)
]
