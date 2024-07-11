from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse
from .models import Blog,Author,Comment
from blog.forms import CommentForm

class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5
    def get_queryset(self):
        return Blog.objects.all().order_by('-created_at')

class BlogDetailView(generic.DetailView):
    model = Blog
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()  
        comments = blog.comments.all()
        context['comments'] = comments
        return context

class BloggerListView(generic.ListView):
    model = Author

class BloggerDetailView(generic.DetailView):
    model = Author
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BloggerDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['blogs'] = Blog.objects.filter(author=context['author']).order_by('-created_at')
        return context
    

def index(request):
    num_blogs = Blog.objects.all().count()
    num_authors = Author.objects.all().count()

    context = {
        'num_blogs': num_blogs,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)

@login_required
def comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comments.all()
    if request.method=='POST':
        form =  CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog  = blog
            comment.author = request.user
            comment.save()
            # redirect to a new URL:
            return redirect('blog-detail',pk=pk)

    # If this is a GET (or any other method) create the default form.
    else:
        form = CommentForm()

    context = {'blog': blog, 'comments': comments, 'form': form}

    return render(request, 'blog/comment.html', context)

# def getBlogById(request, pk):
#     try:
#         blog = Blog.objects.get(pk=pk)
#     except Blog.DoesNotExist:
#         raise Http404('Book does not exist')
    
#     return render(request, 'blog/blog_detail.html',context={'blog':blog})