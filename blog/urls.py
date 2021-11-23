from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    PostListView,
    DetailView,
    CategoryListView,
    LoginView,
    RegistrationView,
    TagListView,
    SearchView,
    FilterSortView,
    create_comment,
    create_child_comment
)


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('filter/', FilterSortView.as_view(), name='filter'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', SearchView.as_view(), name='search'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('create-comment/', create_comment, name='comment_create'),
    path('create_comment_child/', create_child_comment, name='comment_child_create'),
    path('detail/<str:slug>/', DetailView.as_view(), name='detail'),
    path('category/<str:slug>/', CategoryListView.as_view(), name='category_list'),
    path('tag/<str:slug>/', TagListView.as_view(), name='tag_list'),
]
