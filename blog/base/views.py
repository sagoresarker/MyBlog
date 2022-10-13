from django.views import generic
from .models import Post
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request):
    top_list = Post.objects.filter(status=1).order_by('-created_on')[:6]
    featured_list = Post.objects.filter(status=1, priority=1).order_by('-created_on')[:4]
    context = {'featured_list':featured_list, 'top_list':top_list}
    return render(request, 'base/home.html', context)

def PostList(request):
    object_list = Post.objects.filter(status=1).order_by('-created_on')
    featured_list = Post.objects.filter(priority=1).order_by('-created_on')
    paginator = Paginator(object_list, 8)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    return render(request,
                  'base/all_post.html',
                  {'page': page,
                   'post_list': post_list})


def post_detail(request, slug):
    template_name = 'base/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
