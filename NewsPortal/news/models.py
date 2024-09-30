from functools import reduce

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Автор"))
    rating = models.IntegerField(default=0, verbose_name=_("Рейтинг"))

    class Meta:
        verbose_name_plural = "Авторы"
        verbose_name = "Автор"

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

    def __str__(self):
        return f"{self.user.username}"


class Category(models.Model):
    title = models.CharField(max_length = 255, unique=True, verbose_name=_("Название"))

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"


    def __str__(self):
        return f"{self.title}"


class Post(models.Model):
    class PostKind(models.TextChoices):
        NEW = "NEW", _("Новость")
        ART = "ART", _("Статья")

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Автор"))
    kind = models.CharField(max_length=3, choices=PostKind, default=PostKind.NEW, verbose_name=_("Тип"))
    created_dt = models.DateTimeField(default=now, editable=False, verbose_name=_("Дата/время создания"))
    title = models.CharField(max_length = 255, unique=True, verbose_name=_("Заголовок"))
    content = models.TextField(verbose_name=_("Содержание"))
    rating = models.IntegerField(default=0, verbose_name=_("Рейтинг"))
    categories = models.ManyToManyField(Category, verbose_name=_("Категории"))

    class Meta:
        verbose_name_plural = "Публикации"
        verbose_name = "Публикация"


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
    def kind_eng_readable(self):
        return 'articles' if self.kind == 'ART' else 'news'

    @property
    def preview(self):
        """
        возвращает начало статьи (предварительный просмотр)
        длиной 124 символа и добавляет многоточие в конце.
        :return: str
        """
        return f'{self.content[:124]}...'

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_("Публикация"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    content = models.TextField(verbose_name=_("Содержание"))
    created_dt = models.DateTimeField(default=now, editable=False, verbose_name=_("Дата/время создания"))
    rating = models.IntegerField(default=0, verbose_name=_("Рейтинг"))

    class Meta:
        verbose_name_plural = "Комментарии"
        verbose_name = "Комментарий"

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

    def __str__(self):
        return f"{self.content[:100]}"

