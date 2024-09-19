from functools import reduce

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        """
        Обновляет рейтинг текущего автора. Расчет рейтинга представлен следующей последовательностью действий:
        1) подсчитывается суммарный рейтинг каждой статьи/новости автора, умноженный на 3;
        2) подсчитывается суммарный рейтинг всех комментариев автора;
        3) подсчитывается суммарный рейтинг всех комментариев к статьям автора;
        4) суммируются результаты по пунктам 1-3
        :return: None
        """
        # суммарный рейтинг постов автора
        posts = Post.objects.filter(author=self)
        posts_rating = reduce(lambda accumulator, post: accumulator + post.rating * 3, posts, 0)

        # суммарный рейтинг собственных комментариев автора
        own_comments = Comment.objects.filter(user_id = self.user_id)
        own_comments_rating = reduce(lambda accumulator, comment: accumulator + comment.rating, own_comments, 0)

        # суммарный рейтинг комментариев к статьям автора
        extern_comments = [Comment.objects.filter(post_id=post.pk)[0] for post in posts]
        posts_comments_rating = reduce(lambda accumulator, comment: accumulator + comment.rating, extern_comments, 0)

        self.rating = posts_rating + own_comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    title = models.CharField(max_length = 255, unique=True)

class Post(models.Model):
    class PostKind(models.TextChoices):
        NEW = "NEW", _("Новость")
        ART = "ART", _("Статья")

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    kind = models.CharField(max_length=3, choices=PostKind, default=PostKind.NEW)
    created_dt = models.DateTimeField(default=now, editable=False)
    title = models.CharField(max_length = 255, unique=True)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        """
        увеличивает рейтинг на единицу.
        :return: None
        """
        self.rating += 1
        self.save()

    def dislike(self):
        """
        уменьшает рейтинг на единицу.
        :return: None
        """
        self.rating -= 1
        self.save()

    @property
    def kind_readable(self):
        return Post.PostKind[self.kind].label

    @property
    def preview(self):
        """
        возвращает начало статьи (предварительный просмотр)
        длиной 124 символа и добавляет многоточие в конце.
        :return: str
        """
        return f'{self.content[:124]}...'

    @property
    def categories_readable(self):
        return ", ".join([_.category.title for _ in PostCategory.objects.filter(post = self)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_dt = models.DateTimeField(default=now, editable=False)
    rating = models.IntegerField(default=0)

    def like(self):
        """
        увеличивает рейтинг на единицу.
        :return: None
        """
        self.rating += 1
        self.save()

    def dislike(self):
        """
        уменьшает рейтинг на единицу.
        :return: None
        """
        self.rating -= 1
        self.save()
