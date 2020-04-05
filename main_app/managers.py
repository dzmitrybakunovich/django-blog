from django.db import models
from django.db.models import Count, Case, When, Q, F, IntegerField
from django.db.models.functions import Cast, Round


class ArticleQuerySet(models.QuerySet):
    def get_like_dislike_percent(self):
        return self.annotate(
            like_count=Count(
                Case(
                    When(
                        Q(like__is_liked=True),
                        then=1
                    ),
                    output_field=IntegerField(),
                ),
            ),
            dislike_count=Count(
                Case(
                    When(
                        Q(like__is_liked=False),
                        then=1
                    ),
                    output_field=IntegerField(),
                ),
            ),
            total_marks=Count('id'),
        ).annotate(
            liked=Round(Cast(F('like_count') * 100.0 / F('total_marks'), IntegerField())),
            disliked=Round(Cast(F('dislike_count') * 100.0 / F('total_marks'), IntegerField())),
        )

    def get_articles(self):
        return self.annotate(
            like_count=Count('like', filter=Q(like__is_liked=True), distinct=True),
            comment_count=Count('comment', distinct=True)
        ).order_by('-date')
