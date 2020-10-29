from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *


class IndexPage(TemplateView):
    def get(self, request, **kwargs):
        article_data = []
        all_articles = Article.objects.all().order_by('-created_at')[:9]
        # becase 'all_article' is an object must add each item of it to a list and show on website from it
        for article in all_articles:
            article_data.append({
                'title': article.title,
                'category': article.category.title, # use 'title' because 'category' has a FK and uses it
                'cover': article.cover.url, # 'cover' is a image than must use from the 'url' of it otherwise it returns an object
                'created_at': article.created_at.date,

            })
            # only must be a dict
        context = {
            'article_data': article_data
        }

        # Must be sent a response to user and this is done with return context to the templates
        return render(request, 'index.html', context)
