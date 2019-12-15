from django.shortcuts import render, redirect
from .models import Article


def index(request):
    first_articles = Article.objects.order_by('order', 'slug').first()
    return redirect('show', slug=first_articles.slug)


def show(request, slug: str):
    to_display = Article.objects.get(slug=slug)

    articles = Article.objects.order_by('order', 'slug').all()

    return render(request, 'help_app/index.html', {
        'articles': articles,
        'to_display': to_display
    })
