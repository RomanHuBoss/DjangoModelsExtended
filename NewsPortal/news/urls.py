from django.urls import path
# Импортируем созданные нами представления
from .views import PostsList, PostDetail, PostsSearch, PostCreate, PostEdit, PostDelete

urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('search/', PostsSearch.as_view(), name='post_search'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='new_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='new_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='new_delete'),
]