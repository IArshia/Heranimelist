from django.contrib import admin
from django.urls import path
from rest_framework_nested import routers
from . import views


# router = routers.DefaultRouter()
# router.register('animes', views.AnimeViewSet, basename='animes')
# router.register('listanimes', views.ListAnimeViewSet, basename='listanimes')


# listanime_router = routers.NestedDefaultRouter(router, 'listanimes', lookup='list')
# listanime_router.register('items', views.ListAnimeItemViewSet, basename='list-items')


# animes_router = routers.NestedDefaultRouter(router, 'animes', lookup='anime')
# animes_router.register('comments', views.CommentViewSet, basename='anime-comments')


# urlpatterns = router.urls + listanime_router.urls 
# urlpatterns += animes_router.urls

urlpatterns = [
    path('', views.AnimeListView.as_view(), name='animes'),
    path('<int:pk>/', views.AnimeDetailView.as_view(), name='anime-detail'),
]