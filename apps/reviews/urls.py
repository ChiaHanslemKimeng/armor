from django.urls import path
from .views import helpful_vote_view, reviews_list_view

urlpatterns = [
    path('', reviews_list_view, name='reviews_list'),
    path('vote/<uuid:review_id>/', helpful_vote_view, name='review_helpful_vote'),
]

