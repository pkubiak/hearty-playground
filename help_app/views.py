from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article


def index(request):
    first_article = Article.objects.order_by('order', 'slug').first()

    if not first_article:
        raise Article.DoesNotExist('Default Article does not exist')

    return redirect('show', slug=first_article.slug)


def show(request, slug: str):
    to_display = Article.objects.get(slug=slug)

    articles = Article.objects.order_by('order', 'slug').all()

    return render(request, 'help_app/index.html', {
        'articles': articles,
        'to_display': to_display
    })
