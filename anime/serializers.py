from rest_framework import serializers
from django.db import transaction
from . models import Anime, ListAnime, ListAnimeItem, Comment
from django.conf import settings

class SimpleCommetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'title', 'content', 'username']
    username = serializers.SerializerMethodField()

    def get_username(self, comment):
        return str(comment.user)


class AnimeSerializer(serializers.ModelSerializer):
    comments = SimpleCommetSerializer(many=True, read_only=True)
    class Meta:
        model = Anime
        fields = ['id', 'animename', 'name', 'summery', 'myanimelist_score', 'score', 'released_date', 'image_url', 'comments']

    animename = serializers.SerializerMethodField()

    def get_animename(self, anime):
        print(str(anime.name))
        return str(anime.name)


class ListAnimeItmeSerializer(serializers.ModelSerializer):
    anime = AnimeSerializer()
    class Meta:
        model = ListAnimeItem
        fields = ['id', 'anime']


class ListAnimeSerializer(serializers.ModelSerializer):
    items = ListAnimeItmeSerializer(many=True, read_only=True)
    class Meta:
        model = ListAnime
        fields = ['id', 'items', 'created_at']


class AddListAnimeItemSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = ListAnimeItem
        fields = ['id', 'anime_id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'anime', 'created_at', 'title', 'content', 'username']
    
    username = serializers.SerializerMethodField()

    def get_username(self, comment):
        return str(comment.user)


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'title', 'content']

    # def update(self, instance, validated_data):
    #     user_id = self.context['user_id']
    #     return super().update(instance, validated_data)

    def save(self, **kwargs):
        anime_id = self.context['anime_id']
        user_id = self.context['user_id']
        self.isinstance =  Comment.objects.create(
            user_id=user_id, anime_id=anime_id, **self.validated_data)
        return self.instance





# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


# class UpdateOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['payment_status']


# class CreateOrderSerializer(serializers.Serializer):
#     cart_id = serializers.UUIDField()

#     def validate_cart_id(self, cart_id):
#         if not Cart.objects.filter(pk=cart_id).exists():
#             raise serializers.ValidationError(
#                 'No cart with the given ID was found.')
#         if CartItem.objects.filter(cart_id=cart_id).count() == 0:
#             raise serializers.ValidationError('The cart is empty.')
#         return cart_id

#     def save(self, **kwargs):
#         with transaction.atomic():
#             cart_id = self.validated_data['cart_id']

#             customer = Customer.objects.get(
#                 user_id=self.context['user_id'])
#             order = Order.objects.create(customer=customer)

#             cart_items = CartItem.objects \
#                 .select_related('product') \
#                 .filter(cart_id=cart_id)
#             order_items = [
#                 OrderItem(
#                     order=order,
#                     product=item.product,
#                     unit_price=item.product.unit_price,
#                     quantity=item.quantity
#                 ) for item in cart_items
#             ]
#             OrderItem.objects.bulk_create(order_items)

#             Cart.objects.filter(pk=cart_id).delete()

#             order_created.send_robust(self.__class__, order=order)

#             return order
