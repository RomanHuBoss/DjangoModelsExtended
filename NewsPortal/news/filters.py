from datetime import  datetime
from django_filters import CharFilter, FilterSet, DateTimeFilter
from .models import Post
from django.forms import DateInput


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
           'title': ['icontains'],
            'categories': ['exact'],
        }

    added_after = DateTimeFilter(
        field_name='created_dt',
        lookup_expr='gt',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'},
        ),
        label="Опубликовано после..."
    )

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['title__icontains'].label="Заголовок содержит"
        self.filters['categories'].label = "Относится к категориям"



