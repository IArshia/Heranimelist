from django.shortcuts import render
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from anime.pagination import DefaultPagination
from .serializers import AnimeSerializer, ListAnimeSerializer, ListAnimeItmeSerializer, CommentSerializer, AddListAnimeItemSerializer, PostCommentSerializer, UpdateCommentSerializer
from .models import Anime, ListAnime, ListAnimeItem, Comment
from .permissions import IsAdminOrReadOnly



class AnimeViewSet(ModelViewSet):
    serializer_class = AnimeSerializer
    queryset = Anime.objects.prefetch_related('comments').all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', 'summery']
    ordering_fields = ['name', 'myanimelist_score', 'released_date']

    
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
    queryset = Comment.objects.select_related('anime').all()


    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH' ,'DELETE']:
            return [IsAuthenticated()]
        else:
            return []
    

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return PostCommentSerializer
        elif self.request.method in ['PATCH','DELETE']:
            return UpdateCommentSerializer
        else:
            return CommentSerializer


    def get_serializer_context(self):
        user_id = self.request.user.id
        anime_id = self.kwargs['anime_pk']
        return {'user_id':user_id, 'anime_id':anime_id}
    
    def destroy(self, request, *args, **kwargs):
        user_id = self.request.user.id
        comment = Comment.objects.get(id=kwargs['pk'])
        if user_id != comment.user.id:
            return Response({'error': 'Comment can not delete.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
    




