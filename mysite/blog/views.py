from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
#def home(request):
#	return render(request, 'home.html', {})

def LikeView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True
	
	return HttpResponseRedirect(reverse('blog:article-detail', args=[str(pk)]))

class HomeView(ListView):
	model = Post
	template_name = 'blog_home.html'
	cats = Category.objects.all()
	ordering = ['-post_date']
	#ordering = ['-id']

	def get_context_data(self, *args, **kwargs):
		cat_menu = Category.objects.all()
		context = super(HomeView, self).get_context_data(*args, **kwargs)
		context["cat_menu"] = cat_menu
		return context

def CategoryListView(request):
	cat_menu_list = Category.objects.all()
	return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})



def CategoryView(request, cats):
	category_posts = Post.objects.filter(category=cats.replace('-', ' '))
	cat_menu = Category.objects.all()
	return render(request, 'categories.html', {
		'cats':cats.replace('-', ' ').title(),
		 'category_posts':category_posts,
		 'cat_menu':cat_menu
		 })


class ArticleDetailView(DetailView):
	model = Post
	template_name = 'article_details.html'

	def get_context_data(self, *args, **kwargs):
		cat_menu = Category.objects.all()
		context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
		
		stuff = get_object_or_404(Post, id=self.kwargs['pk'])
		total_likes = stuff.total_likes()	
		
		liked = False
		if stuff.likes.filter(id=self.request.user.id).exists():
			liked = True

		context["cat_menu"] = cat_menu
		context["total_likes"] = total_likes
		context["liked"] = liked
		return context

class AddPostView(CreateView):
	model = Post
	form_class = PostForm
	template_name = 'add_post.html'
	#fields = '__all__'
	#fields = ('title', 'body')

def add_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = pk
            comment.save()
            return redirect('blog:article-detail', pk)
    else:
        form = CommentForm()

    context = {'form': form}
    return render(request, 'add_comment.html', context)

def remove_comment(request, pk):
    try:
        comment = Comment.objects.get(id=str(pk))
    except Comment.DoesNotExist:
        raise Http404("Comment does not exist")  # Optional: Handle 404 error in a custom way

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:article-detail', pk=comment.post_id)
    
    context = {'comment': comment}
    return render(request, 'article_details.html', context)


class AddCategoryView(CreateView):
	model = Category
	#form_class = PostForm
	template_name = 'add_category.html'
	fields = '__all__'
	#fields = ('title', 'body')

class UpdatePostView(UpdateView):
	model = Post
	form_class = EditForm
	template_name = 'edit_post.html'
	#fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')