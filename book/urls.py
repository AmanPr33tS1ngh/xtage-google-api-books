from django.urls import path

from book.views import *

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('likes/', Likes.as_view(), name='likes'),
    path('recommendations/', Recommendations.as_view(), name='recommendations'),
    path('search_book/', SearchBooksView.as_view(), name='book'),
    path("like_book/", LikeBook.as_view(), name='like_book'),
    path("comment/", CommentAPI.as_view(), name='comment'),
    path("remove_recommendation/", RemoveRecommendation.as_view(), name='remove_recommendation'),
]
