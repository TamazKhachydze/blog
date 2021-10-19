from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey


class Category(models.Model):
    """Категории"""

    name = models.CharField(max_length=100, verbose_name='Категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Tag(models.Model):
    """Теги"""

    name = models.CharField(max_length=100, verbose_name='Теги')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_list', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)


class Post(models.Model):
    """Пост"""

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name='Контент')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Изображение', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category_posts', verbose_name='Категория'
    )
    tags = models.ManyToManyField(Tag, related_name='tags_posts', verbose_name='Теги')
    count_views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    comments = GenericRelation('comment', related_name='post_comments')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created_at',)


class Comment(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Тест комментария')
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name='Родительский комментарий',
        related_name='comment_children',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now=True, verbose_name='Дата создания комментария')
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

