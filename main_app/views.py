import random
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import View, FormView, TemplateView

from .forms import ArticleForm, CommentForm, CustomUserCreationForm
from .models import Article, Comment, Like, CustomUser


class MainPage(View):
    articles_queryset = Article.objects.get_articles()
    comments_queryset = Comment.objects.order_by('-date')
    template_name = 'main_app/basic_page.html'
    AMOUNT_LAST_COMMENTS = 4
    AMOUNT_RANDOM_ARTICLES = 3

    def get_random_articles(self):
        # Get id all articles
        id_articles = list(Article.objects.values_list('id', flat=True))

        # Get random id
        random_ids = random.sample(id_articles, self.AMOUNT_RANDOM_ARTICLES)

        # Get random articles
        articles = self.articles_queryset.filter(id__in=random_ids)

        return articles

    def get(self, request):
        # Random article for main interactive
        random_articles = self.get_random_articles()

        # Last comments
        last_comments = self.comments_queryset[:self.AMOUNT_LAST_COMMENTS]

        # Paginator
        paginator = Paginator(self.articles_queryset, 8)
        page = request.GET.get('page')
        articles = paginator.get_page(page)

        return render(
            request,
            self.template_name,
            {
                'main_article': random_articles[0],
                'main_articles': random_articles[1:3],
                'articles': articles,
                'comments': last_comments,
            },
        )


class UserArticle(View):
    articles_queryset = Article.objects.get_articles()
    comments_queryset = Comment.objects.order_by('-date')
    template_name = 'main_app/articles_created_by_user.html'
    AMOUNT_LAST_COMMENTS = 4

    def get(self, request, **kwargs):
        user = CustomUser.objects.get(username=kwargs['username'])

        # Get last comments
        last_comments = self.comments_queryset[:self.AMOUNT_LAST_COMMENTS]

        # Paginator
        paginator = Paginator(self.articles_queryset.filter(author_id=user.id), 8)
        page = request.GET.get('page')
        articles = paginator.get_page(page)

        return render(
            request,
            self.template_name,
            {
                'articles': articles,
                'comments': last_comments,
                'user': user,
            }
        )


class RegisterFormView(FormView):
    form_class = CustomUserCreationForm
    success_url = "/"
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse(status=404)
        return render(
            request,
            self.template_name,
        )

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class UserView(View):
    # Template name transmitted from url
    template_name = None

    @staticmethod
    def post(request, username):
        user = CustomUser.objects.get(username=username)
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        if request.FILES.get('images'):
            user.avatar = request.FILES.get('images')
        user.save()
        return redirect(
            'user_profile',
            username=username
        )

    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        return render(
            request,
            self.template_name,
            {
                'is_my_profile': request.user.id == user.id,
                'user_article_count': Article.objects.filter(author_id=user.id).count(),
                'user_comment_count': Comment.objects.filter(author_id=user.id).count(),
                'user_likes_count': Like.objects.filter(user_id=user.id, is_liked=True).count(),
                'user': user
            }
        )


class ArticlePage(View):
    form_class = CommentForm
    template_name = 'main_app/article.html'
    AMOUNT_LAST_ARTICLES = 2

    def post(self, request, **kwargs):
        article = Article.objects.get(slug=kwargs['article_slug'])
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', article_slug=kwargs['article_slug'])

    def get(self, request, **kwargs):
        article = Article.objects.get_like_dislike_percent().get(slug=kwargs['article_slug'])
        return render(
            request,
            self.template_name,
            {
                'form': self.form_class,
                'last_articles': Article.objects.filter(
                    author_id=article.author_id
                ).order_by('-date')[:self.AMOUNT_LAST_ARTICLES],
                'article': article,
                'is_liked': Like.objects.filter(article_id=article.id, user_id=request.user.id),
                'all_likes': Like.objects.filter(article_id=article.id, is_liked=True).count(),
                'marks': Like.objects.filter(article_id=article.id).values('is_liked').annotate(
                    count=Count('is_liked')).order_by('-is_liked'),
                'like_percent': article.liked,
                'dislike_percent': article.disliked,
                'comment': Comment.objects.filter(article_id=article.id).order_by('-date'),
            }
        )


class ArticleView(View):
    form_class = ArticleForm
    template_name = 'main_app/article_edit.html'
    request_type = None

    def delete(self, **kwargs):
        article = Article.objects.get(id=kwargs['article_id'])
        article.delete()
        return redirect('/')

    def post(self, request, **kwargs):
        form = ArticleForm(request.POST, request.FILES)

        # If create new article
        if self.request_type == 'CREATE':
            if form.is_valid():
                article = form.save(commit=False)
                article.author = request.user
                article.save()
                return redirect(
                    'article_detail',
                    article_slug=article.slug
                )

        # If edit article
        elif self.request_type == 'UPDATE':
            article = get_object_or_404(Article, slug=kwargs['article_slug'])
            article.title = request.POST.get('title')
            article.text = request.POST.get('text')
            article.short_description = request.POST.get('short_description')
            if request.FILES.get('images'):
                article.image = request.FILES.get('images')
            article.save()
            return redirect(
                'article_detail',
                article_slug=article.slug
            )

    def get(self, request, **kwargs):
        article = get_object_or_404(
            Article,
            slug=kwargs['article_slug']
        ) if 'article_slug' in kwargs else None
        return render(
            request,
            'main_app/article_edit.html',
            {
                'article': article,
                'form': self.form_class(request.POST or None, request.FILES or None, instance=article),
                'type': self.request_type,
            }
        )


class LikeDislike(View):
    # Vote type transmitted from url
    vote_type = None

    def get(self, request, article_id):
        Like.objects.create(user_id=request.user.id, article_id=article_id, is_liked=self.vote_type)
        return redirect(
            'article_detail',
            article_slug=Article.objects.get(id=article_id).slug
        )


def get_online(request):
    try:
        user = CustomUser.objects.get(pk=request.user.id)
        user.last_online = timezone.now()
        user.save()
        return HttpResponse({'status': 'Success'})
    except CustomUser.DoesNotExist:
        return HttpResponse({'status': 'Fail'})
