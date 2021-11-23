from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Count
from django.shortcuts import render, redirect
from django import views
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
import json
from django.db.models import F
from django.contrib import messages
from django.core.cache import cache

from .models import Post, Tag, Category, Comment
from .forms import LoginForm, RegistrationForm, CommentForm
from .utils import get_path_for_filter_pagination, get_data_for_filter, create_comment_tree, get_data_comment


class CategoryTag:
    """Категории и теги фильмов"""

    def get_categories(self):
        get_categories = cache.get('get_categories')
        if not get_categories:
            get_categories = Category.objects.annotate(cnt=Count('category_posts')).filter(cnt__gt=0)
            cache.set('get_categories', get_categories, 30)
        return get_categories

    def get_tags(self):
        get_tags = cache.get('get_tags')
        if not get_tags:
            get_tags = Tag.objects.annotate(cnt=Count('tags_posts')).filter(cnt__gt=0)
            cache.set('get_tags', get_tags, 30)
        return get_tags


class PostListView(CategoryTag, views.generic.ListView):

    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    slug_url_kwarg = 'slug'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('category')


class DetailView(CategoryTag, views.generic.DetailView):

    model = Post
    context_object_name = 'post'
    template_name = 'blog/single.html'
    # slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = Comment.objects.select_related('user').filter(object_id=kwargs.get('object').id)
        data_comment = get_data_comment(qs)
        context['comments'] = create_comment_tree(**data_comment)
        context['comment_form'] = CommentForm(self.request.POST or None)
        kwargs.get('object').count_views = F('count_views') + 1
        kwargs.get('object').save()
        return context


class CategoryListView(CategoryTag, views.generic.ListView):

    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    slug_url_kwarg = 'slug'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(is_published=True, category__slug=self.kwargs['slug'])


class TagListView(CategoryTag, views.generic.ListView):

    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    slug_url_kwarg = 'slug'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(is_published=True, tags__slug=self.kwargs['slug'])


class LoginView(views.View):

    def get(self, request, *args, **kwargs):
        if request.session.get('previous_page'):
            messages.info(request, 'Чтобы оставлять комментарий сначала нужно Авторизоваться/Зарегестрироватся')
            del request.session['previous_page']
        form = LoginForm(request.POST or None)
        messages.info(request, '')
        context = {
            'form': form,
        }
        return render(request, 'blog/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'blog/login.html', context)


class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'blog/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'blog/registration.html', context)


class SearchView(CategoryTag, views.generic.ListView):

    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 2

    def get_queryset(self):
        print(self.request.GET.get('search'))
        return Post.objects.filter(title__icontains=self.request.GET.get('search')).select_related('category')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = f"search={self.request.GET.get('search')}&"
        return context


class FilterSortView(CategoryTag, views.generic.ListView):

    context_object_name = 'posts'
    template_name = 'blog/index.html'
    model = Post
    paginate_by = 3

    def get_queryset(self):
        kwargs = {}
        if self.request.GET.getlist("category"):
            kwargs["category__slug__in"] = self.request.GET.getlist("category")
        if self.request.GET.getlist("tags"):
            kwargs["tags__slug__in"] = self.request.GET.getlist("tags")
        return Post.objects.filter(**kwargs).order_by(self.request.GET.get('sort')).select_related('category')

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        kwargs = {}
        if self.request.GET.getlist("category"):
            kwargs["category"] = self.request.GET.getlist("category")
        if self.request.GET.getlist("tags"):
            kwargs["tags"] = self.request.GET.getlist("tags")
        kwargs['sort'] = self.request.GET.getlist('sort')
        context['filter_data'] = json.dumps(get_data_for_filter(kwargs))
        context['filter_path'] = get_path_for_filter_pagination(kwargs)
        return context


def create_comment(request):
    if request.user.is_authenticated:
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.text = comment_form.cleaned_data['text']
            new_comment.content_type = ContentType.objects.get(model='post')
            new_comment.object_id = int(request.POST.get('post_id'))
            new_comment.parent = None
            new_comment.is_child = False
            new_comment.save()
        post_slug = Post.objects.get(id=request.POST.get('post_id')).slug
        return HttpResponseRedirect(r'/detail/'+post_slug+'/')
    else:
        request.session['previous_page'] = True
        return redirect('/login/')


@transaction.atomic
def create_child_comment(request):
    user_name = request.POST.get('user')
    current_id = request.POST.get('id')
    text = request.POST.get('text')
    object_id = request.POST.get('postId')
    user = User.objects.get(username=user_name)
    content_type = ContentType.objects.get(model='post')
    parent = Comment.objects.get(id=int(current_id))
    is_child = True
    Comment.objects.create(
        user=user, text=text, content_type=content_type, object_id=object_id, parent=parent, is_child=is_child
    )
    # comments_ = Post.objects.get(id=object_id).comments.all()
    # comments_list = create_comment_tree(comments_)
    qs = Comment.objects.select_related('user').filter(object_id=request.POST.get('postId'))
    data_comment = get_data_comment(qs)
    comments_list = create_comment_tree(**data_comment)
    return render(request, 'blog/single.html', {'comments': comments_list})
