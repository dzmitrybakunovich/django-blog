from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Article, Comment


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'image_in_admin',
    ]
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {'fields': ('avatar',)},
        ),
    )


class ArticleInLine(admin.StackedInline):
    model = Comment
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'image',
        'text',
        'date',
    ]
    inlines = [ArticleInLine]


admin.site.register(Article, ArticleAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
