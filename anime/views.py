from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import AnimeSerializer, ListAnimeSerializer, ListAnimeItmeSerializer, CommentSerializer, AddListAnimeItemSerializer, PostCommentSerializer
from .models import Anime, ListAnime, ListAnimeItem, Comment



class AnimeViewSet(ModelViewSet):
    serializer_class = AnimeSerializer
    queryset = Anime.objects.prefetch_related('comments').all()


class ListAnimeViewSet(ModelViewSet):
    serializer_class = ListAnimeSerializer
    queryset = ListAnime.objects.prefetch_related('items__anime').all()


class ListAnimeItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddListAnimeItemSerializer
        return ListAnimeItmeSerializer

    def get_serializer_context(self):
        return {'list_id': self.kwargs['list_pk']}

    def get_queryset(self):
        return ListAnimeItem.objects \
            .filter(list_id=self.kwargs['list_pk']) \
            .select_related('anime')



class CommentViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    queryset = Comment.objects.prefetch_related('comments__anime').all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH' ,'DELETE']:
            return [IsAuthenticated()]
        else:
            return []
    

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH' ,'DELETE']:
            return PostCommentSerializer
        else:
            return CommentSerializer


    def get_serializer_context(self):
        user_id = self.request.user.id
        anime_id = self.kwargs['anime_pk']
        return {'user_id':user_id, 'anime_id':anime_id}
    




