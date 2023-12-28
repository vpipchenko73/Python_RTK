from django.urls import path
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('news_all/', views.news_all, name = 'news_all' ),
    path('news/', views.test, name = 'news_test' ),
    #path('news_detail/', views.news_detail, name = 'news_detail' ),
    path('news/<int:pk>/', views.ArticleDetailView.as_view(), name='news_detail'),
    path('news_create/', views.ArticleCreateView.as_view(), name='news_create'),#ссылка на создание новости
    path('calc/<int:a>/<slug:operation>/<int:b>', views.calc),
    path('create1', views.create_article, name='news_create1'),
    path('update/<int:pk>', views.ArticleUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', views.ArticleDeleteView.as_view(), name='news_delete'),
    #path('logout', auth_views.LogoutView.as_view( template_name='main/index.html' ), name='logout'),
    path('logout/', views.logout_view, name = 'logout' ),


]
