from django.forms import ModelForm
from .models import Post

class PostAddEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ["author", "title", "content", "categories"]

