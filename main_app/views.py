from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import ArticleForm, CommentForm
from .models import Article, Comment, CustomUser


def main_page(request):
    all_articles = Article.objects.annotate(Count('comment')).order_by('-date')
    main_articles = Article.objects.annotate(Count('comment')).order_by('-date')[:2]
    main_article = Article.objects.annotate(Count('comment')).get(id=4)
    AMOUNT_LAST_COMMENTS = 4
    last_comments = Comment.objects.order_by('-date')[:AMOUNT_LAST_COMMENTS]
    paginator = Paginator(all_articles, 8)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(
        request,
        'main_app/basic_page.html',
        {
            'main_article': main_article,
            'main_articles': main_articles,
            'articles': articles,
            'comment': last_comments,
        },
    )


# page article with comments
def page_article(request, article_id=1):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article_id = article_id
            comment.author_id = request.user.id
            comment.date = timezone.now()
            comment.save()
            return redirect('article_detail', id=article_id)
    else:
        form = CommentForm()
    return render(
        request,
        'main_app/article.html',
        {
            'form': form,
            'article': Article.objects.get(id=article_id),
            'comment': Comment.objects.filter(article_id=article_id).order_by('-date'),
        }
    )


def new_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author_id = request.user.id
            article.date = timezone.now()
            article.save()
            return redirect(
                'article_detail',
                article_id=article.id
            )
    else:
        form = ArticleForm(request.POST, request.FILES)
    return render(
        request,
        'main_app/article_edit.html',
        {
            'form': form
        }
    )


def user_profile(request, user_id=1):
    user = CustomUser.objects.get(id=user_id)
    return render(
        request,
        'main_app/user_profile.html',
        {
            'is_my_profile': request.user.id == user.id,
            'user_article_count': Article.objects.filter(author_id=user_id).count(),
            'user_comment_count': Comment.objects.filter(author_id=user_id).count(),
            'user': user,
        }
    )


def edit(request):
    user_id = request.user.id
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.avatar = request.FILES.get('image')
        user.save()
    return render(
        request,
        'main_app/edit_user_profile.html',
        {
            'user': user
        },
    )


def article_created_by_user(request, user_id=1):
    AMOUNT_LAST_COMMENTS = 4
    last_comments = Comment.objects.order_by('-date')[0:AMOUNT_LAST_COMMENTS]
    all_article = Article.objects.annotate(Count('comment')).filter(author_id=user_id).order_by('-date')
    paginator = Paginator(all_article, 8)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(
        request,
        'main_app/articles_created_by_user.html',
        {
            'articles': articles,
            'comment': last_comments,
            'user': CustomUser.objects.get(id=user_id),
        }
    )
