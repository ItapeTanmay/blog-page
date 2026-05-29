from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post,Like, Comment
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.

def post_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)

    if category:
        posts = posts.filter(category=category)

    posts = posts.order_by('-created_at')

    # Pagination: 6 posts per page
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'category': category,
        'category_choices': Post.CATEGORY_CHOICES,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('post-detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post Created Successfully')
            return redirect('post-detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html',{'form':form,'action':'create'})

@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Restrict to author only
    if post.author != request.user:
        messages.error(request,'You can only edit your own posts.')
        return redirect('post-detail',slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, instance = post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully")
            return redirect('post-detail', slug = post.slug)
    else:
        form = PostForm(instance=post)
    return render(request,'blog/post_form.html',{"form":form,'action':'Update'})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # restricted to author only
    if post.author!=request.user:
        messages.error(request,"You can only delete your own posts ")
        return redirect('post-detail',slug=slug)

    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post Deleted Successfully!')
        return redirect('post-list')

    return render(request, 'blog/post_confirm_delete.html',{'post':post})

@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug = slug)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        # if already liked remove like
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse(
        {
            'liked':liked,
            'like_count':post.likes.count()
        }
    )

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('post-detail', slug=comment.post.slug)

    post_slug = comment.post.slug
    comment.delete()
    messages.success(request, 'Comment deleted.')
    return redirect('post-detail', slug=post_slug)