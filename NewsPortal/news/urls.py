from django.urls import path
# Импортируем созданные нами представления
from .views import PostsList, PostDetail, PostsSearch

urlpatterns = [
   path('', PostsList.as_view()),
   path('search/', PostsSearch.as_view()),
   path('<int:pk>/', PostDetail.as_view()),
]