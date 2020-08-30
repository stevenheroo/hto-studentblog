from django.shortcuts import render

from operator import attrgetter

from blog.models import BlogPost
from blog.views import blog_queryset_search


# Create your views here.
def home_screen_view(request):

	context = {}

	#search bar
	query = ""
	if request.GET:
		query = request.GET['q']



	#Sorts the blog posted in referrence to the Keygetter...
	blog_posts = sorted(blog_queryset_search(query), key=attrgetter('date_updated'), reverse=True)
	context = {
		'blog_posts':blog_posts,
		'query': str(query),
	}


	return render(request, 'firstpage/home.html', context )