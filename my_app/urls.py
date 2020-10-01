from django.urls import path
from . import views

app_name = 'my_app'


urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('search_by_rollno', views.search_by_rollno, name='search_by_rollno'),
    path('parse_search_rollno', views.parse_search_rollno, name='parse_search_rollno')
]