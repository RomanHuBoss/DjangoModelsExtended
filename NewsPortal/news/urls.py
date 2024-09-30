from django.urls import path
# Импортируем созданные нами представления
from .views import PostsList, PostDetail, PostsSearch, PostCreate, PostEdit, PostDelete

urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('search/', PostsSearch.as_view()),
   path('<int:pk>/', PostDetail.as_view()),
   path('create/', PostCreate.as_view()),
   path('<int:pk>/edit/', PostEdit.as_view()),
   path('<int:pk>/delete/', PostDelete.as_view()),
]