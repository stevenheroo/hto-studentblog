from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse 


from accounts.models import Account
from blog.models import BlogPost , Like
from blog.forms import CreateBlogPostForm, UpdateBlogForm



# Create your views here.
def create_blog_view(request):

	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	#IF user is Authenticated, will be abe to create Post
	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		context['prompt_success'] = 'Blog Created'
		form = CreateBlogPostForm()

	context['form'] = form

	#Show Blog that belongs to the author in profile page,
	blog_posts = BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts
	return render(request,"blog/create_blog.html", context)



#Detail Blog
def detail_blog_view(request, slug):

	blog_posts = get_object_or_404(BlogPost, slug=slug)
	user = request.user
	context = {
		'blog_posts' : blog_posts,
		'user' : user,
	}

	return render(request, 'blog/detail_blog.html', context)



#Like Blog
def like_blog_view(request, slug):
	user = request.user
	if request.method == 'POST':
		blog_id = request.POST.get('blog_id')
		blog_posts = BlogPost.objects.get(id=blog_id)

			#if user is already in ManyToMany view then remove user from like field
		if user in blog_posts.likes.all():
			blog_posts.likes.remove(user)
		else:#if user is not in ManyToMany view then add user to like field
			blog_posts.likes.add(user)


		like, created = Like.objects.get_or_create(user=user, blog_id=blog_id)

		if not created:
			if like.value == 'Like':
				like.value = 'Unlike'
			else:
				like.value = 'Like'
		like.save()

	return redirect('blog:detail', slug=slug)



#Edit Blog 
def edit_blog_view(request, slug):

	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	blog_post = get_object_or_404(BlogPost, slug=slug)
	form = UpdateBlogForm(request.POST or None, request.FILES or None, instance=blog_post)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		context['prompt_success'] = "Updated"
		blog_post = obj

	form = UpdateBlogForm(
		initial = {
			"title" : blog_post.title,
			"body" : blog_post.body,
			"image" : blog_post.image,
		}
	)
	context['form'] = form
	return render(request, 'blog/edit_blog.html', context)




def blog_queryset_search(query=None):
	queryset = []
	queries = query.split(" ") #removes white spaces and group each word into List
	
	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) | Q(body__icontains=q)

			).distinct() # all retrived post to be unique

		for post in posts:
			queryset.append(post)

	return list(set(queryset))