from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Post
from .forms import PostForm, RegisterForm


# ---------------------------------------------------------------------
# 1. REGISTRATION         
# ---------------------------------------------------------------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()              # creates the User row (password hashed automatically)
            login(request, user)             # logs the new user in immediately
            messages.success(request, f'Welcome, {user.username}! Your account was created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'posts/register.html', {'form': form})


# ---------------------------------------------------------------------
# 2. LOGIN / LOGOUT
# Django ships with class-based LoginView/LogoutView - we just point
# them at our own template and add a success message.
# ---------------------------------------------------------------------
class CustomLoginView(LoginView):
    template_name = 'posts/login.html'

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


# ---------------------------------------------------------------------
# 3. HOME PAGE - list all posts + search by title/caption
# ---------------------------------------------------------------------
def home_view(request):
    query = request.GET.get('q', '').strip()
    posts = Post.objects.select_related('author').all()  # select_related avoids extra DB queries

    if query:
        # Q objects let us build an OR condition across two fields
        posts = posts.filter(Q(title__icontains=query) | Q(caption__icontains=query))

    paginator = Paginator(posts, 9)  # 9 posts per page, Instagram-grid style
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/home.html', {
        'page_obj': page_obj,
        'query': query,
    })


# ---------------------------------------------------------------------
# 4. CREATE a post (must be logged in)
# ---------------------------------------------------------------------
@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # request.FILES is required for uploads
        if form.is_valid():
            post = form.save(commit=False)   # don't save yet - need to set author first
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {'form': form, 'action': 'Create'})


# ---------------------------------------------------------------------
# 5. EDIT a post (only the owner can edit)
# ---------------------------------------------------------------------
@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {'form': form, 'action': 'Edit', 'post': post})


# ---------------------------------------------------------------------
# 6. DELETE a post (only the owner can delete) - confirm first
# ---------------------------------------------------------------------
@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, "You don't have permission to delete this post.")
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')

    return render(request, 'posts/post_confirm_delete.html', {'post': post})


# ---------------------------------------------------------------------
# 7. POST DETAIL (view a single post - optional but handy)
# ---------------------------------------------------------------------
def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})
