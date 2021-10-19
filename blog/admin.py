from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Post, Tag, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.contenttypes.admin import GenericTabularInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
    fields = (('name', 'slug',),)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
    fields = (('name', 'slug',),)


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(label='Контент', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostCommentsInline(GenericTabularInline):
    extra = 1
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_image', 'get_comments')
    list_display_links = ('id', 'title',)
    list_filter = ('category', 'tags')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at', 'get_image', 'count_views')
    list_editable = ('is_published',)
    save_as = True
    save_on_top = True
    form = PostAdminForm
    inlines = [
        PostCommentsInline
    ]
    fieldsets = (
        (None, {
            'fields': (('title', 'slug', 'category', 'tags'), ),
            'classes': ('wide',)
        }),
        (None, {
            'fields': (('get_image', 'image',), 'content',),
            'classes': ('wide',)
        }),
        (None, {
            'fields': (('created_at', 'updated_at', 'count_views', 'is_published'), ),
            'classes': ('wide',)
        }),

    )

    def get_image(self, obj):
        if not obj.image:
            return mark_safe('<img src="/static/blog/img/blog-image1.jpg" width="100" height="auto">')
        return mark_safe(f'<img src={obj.image.url} width="100" height="100">')

    def get_comments(self, obj):
        print(obj.comments.all())
        pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('user', 'text', 'timestamp', 'is_child', 'parent')
    readonly_fields = ('user', 'text', 'timestamp', 'is_child', 'parent')
    list_display_links = ('user',)