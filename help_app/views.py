from django.shortcuts import render, redirect
from .models import Article


def does_not_exists(request):
    return render(request, 'help_app/does_not_exists.html',
        {'all_articles': Article.all_articles()},
        status=404
    )


def index(request):
    first_article = Article.objects.order_by('order', 'slug').first()

    if not first_article:
        return does_not_exists(request)

    return redirect('help_app:show', slug=first_article.slug)


def show(request, slug: str):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        return does_not_exists(request)

    return render(request, 'help_app/show.html', {
        'all_articles': Article.all_articles(),
        'article': article,
    })
