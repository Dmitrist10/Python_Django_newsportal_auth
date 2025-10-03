from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # path("news/create", create_New, name=""),
    # path("articles/create", create_Article, name=""),


    path('news/<int:pk>', New_Detail.as_view(), name="New_Detail"),
    path('news/', New_List.as_view(), name="New_List"),
    path("news/create", News_Form_Create.as_view(), name="News_Form_Create"),
    path("news/<int:pk>/edit", News_Form_Edit.as_view(), name="News_Form_Edit"),
    path("news/<int:pk>/delete", News_Form_Delete.as_view(), name="News_Form_Delete"),

    path('articles/<int:pk>', Article_Detail.as_view(), name="Article_Detail"),
    path('articles/', Article_List.as_view(), name="Article_List"),
    path("articles/create", Articles_Form_Create.as_view(), name="Article_Form_Create"),
    path("articles/<int:pk>/edit",
         Articles_Form_Edit.as_view(), name="News_Form_Edit"),
    path("articles/<int:pk>/delete", Articles_Form_Delete.as_view(), name="News_Form_Delete"),

    path('authors/<int:pk>', Author_Detail.as_view()),
    path('authors/', Author_List.as_view()),

    path('home/', HomePage.as_view(), name="HomePage"),
    path('mypage/', MyPage.as_view(), name="MyPage"),

    path('upgrade/', upgrade_me, name='upgrade'),
    path('startAuthor/', startAuthor, name='startAuthor')
]
