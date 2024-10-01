from django.urls import path
# Импортируем созданные нами представления
from .views import PostsList, PostDetail, PostsSearch, PostDelete, PostCreate, PostEdit

urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('search/', PostsSearch.as_view(), name='post_search'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
]