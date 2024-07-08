
from django.urls import path
from . import views
from .views import HomeView, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, AddCategoryView, CategoryView, CategoryListView, LikeView
 
app_name = 'blog'
urlpatterns = [
    path('blog_home/', HomeView.as_view(), name="blog_home"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='edit_post'),
    path('article/<int:pk>/remove', DeletePostView.as_view(), name='delete_post'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('category-list/', CategoryListView, name='category-list'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('article/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('remove-comment/<int:pk>/', views.remove_comment, name='remove-comment'),
    ]
