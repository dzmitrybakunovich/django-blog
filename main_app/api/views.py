from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Article, CustomUser
from .serializers import ArticleSerializer


class ArticleView(APIView):

    @staticmethod
    def get(request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({'articles': serializer.data})

    @staticmethod
    def post(request):
        article = request.data.get('article')
        serializer = ArticleSerializer(data=article)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
            return Response({"success": "Article created successfully".format(article_saved.title)})