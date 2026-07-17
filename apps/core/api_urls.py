from django.urls import path
from .views import autocomplete_search_view

urlpatterns = [
    path('search/autocomplete/', autocomplete_search_view, name='api_search_autocomplete'),
]
