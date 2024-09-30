from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, DeleteView
from .models import Post
from .filters import PostFilter

class PostCreate(FormView):
    pass

class PostEdit(FormView):
    pass

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class PostsList(ListView):
    model = Post
    ordering = '-created_dt'
    template_name = 'news.html'
    context_object_name = 'posts_list'
    paginate_by = 10

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

class PostsSearch(ListView):
    model = Post
    ordering = '-created_dt'
    template_name = 'search.html'
    context_object_name = 'posts_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['filterset'] = self.filterset
       context['active_filters_quantity'] = list(filter(lambda param: len(self.request.GET[param]) != 0, self.request.GET))
       return context