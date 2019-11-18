from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics

from ..models import Article
from .serializers import ArticleSerializer


class AddAuthorInArticle(APIView):

    def post(self, request, pk, format=None):
        article = Article.objects.get(pk=pk)
        article.author.add(request.user)
        return Response({'author_add': True})


class ArticleList(generics.ListAPIView):
    queryset = Article.objects.all().order_by('id')
    serializer_class = ArticleSerializer


class ArticleDetail(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
