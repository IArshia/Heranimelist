from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.db.models.aggregates import Count
from django.views.generic.edit import FormMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, renderers
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from anime.pagination import DefaultPagination
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
    ordering = ['id']

    renderer_classes = [renderers.TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        self.template_name = 'anime/anime_list.html'
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        self.template_name = 'anime/anime_detail.html'
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        querySet_list = ListAnime.objects.filter(user=self.request.user).all()
        serializer_list = ListAnimeSerializer(querySet_list, many=True)
        serializer_comment = PostCommentSerializer()
        serializer_item = AddListAnimeItemSerializer({'anime_id': self.kwargs['pk']})
        return Response({
            'serializer': serializer_comment, 
            'serializer_item':serializer_item, 
            'anime': serializer.data, 
            'lists': serializer_list.data
            })

    


    
class ListAnimeViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get_queryset(self):
        return ListAnime.objects.filter(user_id=self.request.user.id).all()

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        self.template_name = 'anime/list_anime_list.html'

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer_2 = AddListAnimeSerializer()
        return Response({'serializer': serializer_2, 'lists': serializer.data})
    
    def retrieve(self, request, *args, **kwargs):
        self.template_name = 'anime/list_anime_detail.html'
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer_item = AddListAnimeItemSerializer()
        return Response({'serializer': serializer_item, 'list': serializer.data})
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return redirect('listanimes-list')
    


class ListAnimeItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddListAnimeItemSerializer
        return ListAnimeItmeSerializer

    def get_serializer_context(self):
        return {'list_id': self.kwargs['list_pk']}

    def get_queryset(self):
        return ListAnimeItem.objects.filter(list_id=self.kwargs['list_pk']).all()
    
    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id
        list = ListAnime.objects.get(id=kwargs['list_pk'])
        if user_id != list.user.id:
            return Response({'error': 'List item can not add because this is not for you.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print(request.data)
        # return redirect('listanimes-detail', self.kwargs['list_pk'])
        return redirect('animes-detail', request.data['anime_id'])

    def destroy(self, request, *args, **kwargs):
        user_id = self.request.user.id
        list_item = ListAnimeItem.objects.get(id=kwargs['pk'])
        if user_id != list_item.list.user.id:
            return Response({'error': 'List item can not delete because this is not for you.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)



class CommentViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    # pagination_class = DefaultPagination
    filter_backends = [OrderingFilter]
    ordering = ['id']

    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get_queryset(self):
        return Comment.objects.filter(anime_id=self.kwargs['anime_pk']).all()

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
        user = self.request.user
        anime_id = self.kwargs['anime_pk']
        return {'user':user, 'anime_id':anime_id}
    
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
    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        self.template_name = 'anime/anime_comments_list.html'

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer_2 = PostCommentSerializer()
        return Response({'serializer': serializer_2, 'results': serializer.data})
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return redirect('animes-detail', self.kwargs['anime_pk'])
    
    
    
    


# ApiViews



# class AnimeListView(ListView):
#     model = Anime
#     template_name = 'anime/anime_list.html'
#     context_object_name = 'animes'
#     paginate_by = 21

#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         object_list = self.model.objects.all()
#         if query:
#             object_list = self.model.objects.filter(name__icontains=query)
#         return object_list
    


# class AnimeDetailView(FormMixin, DetailView):
#     model = Anime
#     template_name = 'anime/anime_detail.html'
#     context_object_name = 'anime'
#     form_class = CommentForm

#     def get_success_url(self):
#         return reverse("anime-detail", kwargs={"pk":self.object.id})

#     def get_context_data(self, **kwargs):
#         context = super(AnimeDetailView, self).get_context_data(**kwargs)
#         context["form"] = CommentForm(initial={"anime":self.object, "user":self.request.user})
#         return context

#     def post(self, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             pass

#     def form_valid(self, form):
#         form.save()
#         return super(AnimeDetailView, self).form_valid(form)
    

# class ListAnimeView(ListView):
#     model = ListAnime
#     template_name = 'anime/list_anime.html'
#     context_object_name = 'list_anime'

#     def get_queryset(self) -> QuerySet[Any]:
#         object_list = self.model.objects.filter(user=self.request.user)
#         return object_list


  

