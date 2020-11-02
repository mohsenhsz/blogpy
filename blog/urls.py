from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexPage.as_view(), name='index'),

    # define a new url for contact_page this url uses from 'ContactPage' view that We have to build on 'views.py'
    url(r'^contact/$', views.ContactPage.as_view(), name='contact'),
    url(r'^about/$', views.AboutPage.as_view(), name='about'),
    url(r'^category/$', views.CategoryPage.as_view(), name='category'),
    # APIs URL
    url(r'^article/all/$', views.AllArticleAPIView.as_view(), name='all_article'),
    url(r'^article/$', views.SingleArticleAPIView.as_view(), name='single_article'),
    url(r'^article/search/$', views.SearchArticleAPIView.as_view(), name='article_search'),
    url(r'^article/submit/$', views.SubmitArticleAPIView.as_view(), name='article_submit'),
    url(r'^article/update_cover/$', views.UpdateArticleCoverAPIView.as_view(), name='article_cover_update'),
    url(r'article/delete/$', views.DeleteArticleAPIView.as_view(), name='article_delete'),
]
