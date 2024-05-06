from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from core.utils import upload_image
from .models import CollectionItem, UserCollection
from .serializers import CollectionItemSerializer, CollectionCreateSerializer, UserCollectionCreateSerializer


class CollectionsViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action == 'collection_create_get' or self.action == 'collection_create_post':
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (AllowAny,)
        return tuple(permission() for permission in self.permission_classes)

    def get_serializer_class(self):
        if self.action == 'collection_create_get' or self.action == 'collection_create_post':
            self.serializer_class = CollectionCreateSerializer
        self.serializer_class = CollectionCreateSerializer
        return self.serializer_class

    @action(detail=True)
    def get_collection_by_id(self, request, *args, **kwargs):
        collection_id = kwargs.get('collection_id')
        collection_items = get_object_or_404(CollectionItem, collection_id=collection_id)
        serializer = CollectionItemSerializer(collection_items, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def collection_create_get(self, request, *args, **kwargs):
        return Response({"name": ''})

    @action(detail=True)
    def collection_create_post(self, request, *args, **kwargs):
        serializer = CollectionCreateSerializer(data=request.data)
        if serializer.is_valid():
            collection = serializer.save()
            user_collection_serializer = UserCollectionCreateSerializer(user=request.user, collection=collection)
            if user_collection_serializer.is_valid():
                user_collection_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionsItemViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action == 'collection_item_create_get' or self.action == 'collection_item_create_post':
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (AllowAny,)
        return tuple(permission() for permission in self.permission_classes)

    def get_serializer_class(self):
        if self.action == 'collection_item_create_get' or self.action == 'collection_item_create_post':
            self.serializer_class = CollectionItemSerializer
        self.serializer_class = CollectionItemSerializer
        return self.serializer_class

    @action(detail=True)
    def collection_item_create_get(self, request, *args, **kwargs):
        return Response({"name": ''})

    @action(detail=True)
    def collection_item_create_post(self, request, *args, **kwargs):
        img = request.data['img']
        image_url = upload_image(img, 'collection')
        data = {
            'description': request.data['description'],
            'image_url': image_url,
            'collection': kwargs.get('collection_id'),
        }
        collection = CollectionItemSerializer(data=data)
        if collection.is_valid():
            collection.save()
            return Response(collection.data, status=status.HTTP_201_CREATED)
        return Response(collection.errors, status=status.HTTP_400_BAD_REQUEST)
