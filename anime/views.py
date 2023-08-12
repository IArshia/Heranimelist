from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.db.models.aggregates import Count
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, renderers
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from anime.pagination import DefaultPagination
from .forms import CommentForm, ListAnimeForm
from .serializers import AnimeSerializer, ListAnimeSerializer, AddListAnimeSerializer, UpdateListAnimeSerializer, ListAnimeItmeSerializer, CommentSerializer, AddListAnimeItemSerializer, PostCommentSerializer, UpdateCommentSerializer
from .models import Anime, ListAnime, ListAnimeItem, Comment
from .permissions import IsAdminOrReadOnly

  

class AnimeViewSet(ModelViewSet):
    serializer_class = AnimeSerializer
    queryset = Anime.objects.prefetch_related('comments').all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['name', 'summery']
    ordering_fields = ['name', 'myanimelist_score', 'released_date']

    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'anime/anime_list.html'

    
    

    
class ListAnimeViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    queryset = ListAnime.objects.select_related('user').all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH' ,'DELETE']:
            return [IsAuthenticated()]
        else:
            return []

    def get_serializer_class(self):
        if self.request.method in ['POST', 'DELETE']:
            return AddListAnimeSerializer
        elif self.request.method == 'PATCH':
            return UpdateListAnimeSerializer
        return ListAnimeSerializer
    
    def get_serializer_context(self):
        user_id = self.request.user.id
        return {'user_id':user_id}

    def destroy(self, request, *args, **kwargs):
        user_id = self.request.user.id
        list = ListAnime.objects.get(id=kwargs['pk'])
        if user_id != list.user.id:
            return Response({'error': 'List can not delete because this is not for you.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        user_id = self.request.user.id
        list = ListAnime.objects.get(id=kwargs['pk'])
        if user_id != list.user.id:
            return Response({'error': 'List can not be update because this is not for you.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


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
    
    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id
        list = ListAnime.objects.get(id=kwargs['list_pk'])
        if user_id != list.user.id:
            return Response({'error': 'List item can not add because this is not for you.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user_id = self.request.user.id
        list_item = ListAnimeItem.objects.get(id=kwargs['pk'])
        if user_id != list_item.list.user.id:
            return Response({'error': 'List item can not delete because this is not for you.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)



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
            return Response({'error': 'Comment can not delete because this is not for you.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        user_id = self.request.user.id
        Comment = Comment.objects.get(id=kwargs['pk'])
        if user_id != Comment.user.id:
            return Response({'error': 'Comment can not be update because this is not for you.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
    



# class AnimeViewSet(ModelViewSet):
#     serializer_class = AnimeSerializer
#     queryset = Anime.objects.prefetch_related('comments').all()
#     permission_classes = [IsAdminOrReadOnly]
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     pagination_class = DefaultPagination
#     search_fields = ['name', 'summery']
#     ordering_fields = ['name', 'myanimelist_score', 'released_date']
    
   





# Main Models


class AnimeListView(ListView):
    model = Anime
    template_name = 'anime/anime_list.html'
    context_object_name = 'animes'
    paginate_by = 21

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = self.model.objects.all()
        if query:
            object_list = self.model.objects.filter(name__icontains=query)
        return object_list
    


class AnimeDetailView(FormMixin, DetailView):
    model = Anime
    template_name = 'anime/anime_detail.html'
    context_object_name = 'anime'
    form_class = CommentForm

    def get_success_url(self):
        return reverse("anime-detail", kwargs={"pk":self.object.id})

    def get_context_data(self, **kwargs):
        context = super(AnimeDetailView, self).get_context_data(**kwargs)
        context["form"] = CommentForm(initial={"anime":self.object, "user":self.request.user})
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            pass

    def form_valid(self, form):
        form.save()
        return super(AnimeDetailView, self).form_valid(form)
    

class ListAnimeView(ListView):
    model = ListAnime
    template_name = 'anime/list_anime.html'
    context_object_name = 'list_anime'

    def get_queryset(self) -> QuerySet[Any]:
        object_list = self.model.objects.filter(user=self.request.user)
        return object_list


  

