from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy, resolve
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostAddEditForm

class PostEdit(UpdateView):
    model = Post
    template_name = "post_editor.html"
    form_class = PostAddEditForm
    success_url = "/news/"

    def get(self, request, *args, **kwargs):
        if 'publication_type' in kwargs and kwargs['publication_type'] not in ['news', 'articles']:
            return redirect('/')

        self.publication_type = kwargs['publication_type']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publication_type'] = self.publication_type
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class PostCreate(CreateView):
    model = Post
    template_name = "post_editor.html"
    form_class = PostAddEditForm
    success_url = "/news/"

    def post(self, request, *args, **kwargs):
        if 'publication_type' in kwargs and kwargs['publication_type'] not in ['news', 'articles']:
            return redirect('/')

        self.publication_type = kwargs['publication_type']
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'publication_type' in kwargs and kwargs['publication_type'] not in ['news', 'articles']:
            return redirect('/')

        self.publication_type = kwargs['publication_type']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publication_type'] = self.publication_type
        return context

    def form_valid(self, form):
        form_data = form.save(commit=False)
        form_data.kind = Post.PostKind.ART if self.publication_type == 'articles' else Post.PostKind.NEW
        form_data.save()
        return super().form_valid(form)

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

    def get(self, request, *args, **kwargs):
        if 'publication_type' in kwargs and kwargs['publication_type'] not in ['news']:
            return redirect('/')

        return super().get(request, *args, **kwargs)

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