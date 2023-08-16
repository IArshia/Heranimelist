from rest_framework import serializers
from django.db import transaction
from . models import Anime, ListAnime, ListAnimeItem, Comment
from django.conf import settings

class SimpleCommetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'username', 'content']

    username = serializers.SerializerMethodField()

    def get_username(self, comment: Comment):
        return comment.user.username


class AnimeSerializer(serializers.ModelSerializer):
    comments = SimpleCommetSerializer(many=True, read_only=True)
    class Meta:
        model = Anime
        fields = ['id', 'name', 'summery', 'myanimelist_score', 'score', 'released_date', 'image_url', 'comments']



class ListAnimeItmeSerializer(serializers.ModelSerializer):
    anime = AnimeSerializer()
    class Meta:
        model = ListAnimeItem
        fields = ['id', 'anime']
    


class ListAnimeSerializer(serializers.ModelSerializer):
    items = ListAnimeItmeSerializer(many=True, read_only=True)
    class Meta:
        model = ListAnime
        fields = ['id', 'name', 'user', 'items', 'created_at']


class AddListAnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListAnime
        fields = ['id', 'name']

    def save(self, **kwargs):
        user_id = self.context['user_id']
        self.isinstance =  ListAnime.objects.create(
            user_id=user_id, **self.validated_data)
        return self.instance


class UpdateListAnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListAnime
        fields = ['name']
    


class AddListAnimeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListAnimeItem
        fields = ['id', 'anime_id']
    
    anime_id = serializers.IntegerField()

    def validate_anime_id(self, value):
        if not Anime.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No Anime with the given ID was found.')
        return value


    def save(self, **kwargs):
        list_id = self.context['list_id']
        anime_id = self.validated_data['anime_id']

        try:
            list_anime_item = ListAnimeItem.objects.get(
                list_id=list_id, anime_id=anime_id)
            list_anime_item.save()
            self.instance = list_anime_item
        except ListAnimeItem.DoesNotExist:
            self.instance = ListAnimeItem.objects.create(
                list_id=list_id, **self.validated_data)

        return self.instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'username', 'anime', 'created_at', 'content']

    username = serializers.SerializerMethodField()

    def get_username(self, comment: Comment):
        return comment.user.username


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']
        
    def save(self, **kwargs):
        anime_id = self.context['anime_id']
        user = self.context['user']
        self.isinstance =  Comment.objects.create(
            user=user, anime_id=anime_id, **self.validated_data)
        return self.instance


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']


