from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, CommentForm
from .models import Post, Comment, Like
from django.shortcuts import redirect

@login_required
def feed_view(request):
    posts = Post.objects.select_related('user').order_by('-created_at')

    if request.method == 'POST':
        # create post directly from feed form
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()

    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'feed.html', context)

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'create-post.html', {'form': form})

@login_required
def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related('user').order_by('created_at')

    if request.method == 'POST':
        cform = CommentForm(request.POST)
        if cform.is_valid():
            comment = cform.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        cform = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': cform,
    }
    return render(request, 'post.html', context)

@login_required
def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    existing_like = Like.objects.filter(post=post, user=request.user)

    if existing_like.exists():
        existing_like.delete()  # Unlike
    else:
        Like.objects.create(post=post, user=request.user)  # Like

    return redirect('feed')  # or 'post_detail' if needed