from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers

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
                'created_at': article.created_at.date(),
            })
        promote_data = []
        all_promote_articles = Article.objects.filter(promote=True).order_by('created_at')[:3]
        for promote_article in all_promote_articles:
            promote_data.append({
                'cover': promote_article.cover.url if promote_article.cover else None,
                'title': promote_article.title,
                'category': promote_article.category.title,
                'created_at': promote_article.created_at.date(),
                'author': promote_article.author.user.get_full_name,
                'avatar': promote_article.author.avatar.url if promote_article.author.avatar else None,
            })

            # data that must return to template only must be a dict
        context = {
            'article_data': article_data,
            'promote_article_data': promote_data,
        }

        # for return a html file to user must uses from 'render'
        return render(request, 'index.html', context)


class ContactPage(TemplateView):
    template_name = 'page-contact.html'


class AboutPage(TemplateView):
    template_name = 'page-about.html'


class CategoryPage(TemplateView):
    template_name = 'category.html'


# view for 'all_article' api
class AllArticleAPIView(APIView):

    def get(self, request, format=None):
        try:
            all_articles = Article.objects.all().order_by('-created_at')
            data = []

            for article in all_articles:
                data.append({
                    'title': article.title,
                    'cover': article.cover.url if article.cover else None,
                    'content': article.content,
                    'created_at': article.created_at,
                    'category': article.category.title,
                    'author': article.author.user.first_name + ' ' + article.author.user.last_name,
                    'promote': article.promote,
                })

            return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error We'll Check It Later"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# view for 'article' api that get a articles title and filter it from all articles
class SingleArticleAPIView(APIView):

    def get(self, request, format=None):
        try:
            article_title = request.GET['article_title']
            article = Article.objects.filter(title__contains=article_title)
            serialized = serializers.SingleArticleSerializers(article, many=True)
            data_serialized = serialized.data

            return Response({'data': data_serialized}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error We'll Check It Later"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# a view for 'article_search' api which searches among the content of articles
class SearchArticleAPIView(APIView):

    def get(self, request, format=None):
        try:
            from django.db.models import Q

            query = request.GET['query']
            articles = Article.objects.filter(Q(content__icontains=query))

            '''
            # serialize query with for loop
            data = []
            for article in articles:
                data.append({
                    'title': article.title,
                    'cover' : article.cover.url if article.cover else None,
                    'content' : article.content,
                    'category' : article.category.title,
                    'author' : article.author.user.first_name + ' ' + article.author.user.last_name,
                    'created_at' : article.created_at.date(),
                    'promote' : article.promote,
                })
                '''
            seriallized_query = serializers.ArticleSerializers(articles, many=True)
            data = seriallized_query.data

            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error We'll Check It Later"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# a view for 'article_submit' api that create and insert article into database with post method
class SubmitArticleAPIView(APIView):

    def post(self, request, format=None):
        try:
            # serialize request that resived from post method
            serializer = serializers.SubmitArticleSerializer(data=request.data)
            # check data validation
            if serializer.is_valid():
                title = serializer.data.get('title')
                cover = request.FILES['cover']
                content = serializer.data.get('content')
                category_id = serializer.data.get('category_id')
                author_id = serializer.data.get('author_id')
                promote = serializer.data.get('promote')
            else:
                return Response({'status': 'Bad Request'}, status=status.HTTP_200_OK)
            # convert 'author_id' and 'category_id' to author and category 
            user = User.objects.get(id=author_id)
            author = UserProfile.objects.get(user=user)
            category = Category.objects.get(id=category_id)

            # insert the values taken into their variables
            article = Article() # an object from Article class
            article.title = title
            article.cover = cover
            article.content = content
            article.category = category
            article.author = author
            article.promote = promote
            article.save()

            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error We'll Check It Later"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# a view for 'update_cover_article' api
class UpdateArticleCoverAPIView(APIView):

    def post(self,request, format=None):
        try:
            serializer = serializers.UpdateArticleCoverSerializer(data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
                cover = request.FILES['cover']
            else:
                return Response({'status': 'Bad Request'}, status=status.HTTP_200_OK)

            Article.objects.filter(id=article_id).update(cover=cover)
            
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error We'll Check It Later"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# a view for 'delete_article' api
class DeleteArticleAPIView(APIView):

    def post(self, request, format=None):
        try:
            serializer = serializers.DeleteArticleSerializer(data=request.data)

            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
            else:
                return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

            Article.objects.filter(id=article_id).delete()
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error We'll Check It Later"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
