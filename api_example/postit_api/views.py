from turtle import mode
from django.shortcuts import render
from rest_framework import generics, permissions
from . import models, serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PostList(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        post = models.Post.objects.filter(pk=kwargs['pk'], user=request.user)
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_("you cannot edit this"))

    def delete(self, request, *args, **kwargs):
        post = models.Post.objects.filter(pk=kwargs['pk'], user=request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_("you cannot delete this"))


class CommentList(generics.ListCreateAPIView):
    #queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return models.Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(pk=kwargs['pk'], user=request.user)
        if comment.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_("you cannot edit this comment"))

    def delete(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(pk=kwargs['pk'], user=request.user)
        if comment.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_("you cannot delete this comment"))






