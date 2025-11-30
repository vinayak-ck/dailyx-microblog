from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User   
from .forms import SignUpForm, ProfileForm
from .models import Profile, Follow          
from django.db.models import Q

def landing_view(request):
    # index.html
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    profile = request.user.profile

    is_following = False  
    
    followers_count = request.user.followers.count()
    following_count = request.user.following.count()

    context = {
        "profile": profile,
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count,
    }
    return render(request, "profile.html", context)

@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit-profile.html', {'form': form})

from .models import Profile, Follow

@login_required
def toggle_follow(request, user_id):
    """Follow or unfollow another user."""
    target_user = get_object_or_404(User, id=user_id)

    
    if target_user == request.user:
        return redirect('profile')

    relation, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user,
    )

    
    if not created:
        relation.delete()

    
    next_url = request.META.get('HTTP_REFERER', None)
    if next_url:
        return redirect(next_url)
    return redirect('feed')

@login_required
def search_users(request):
    query = request.GET.get("q", "")

    users = []
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        ).exclude(id=request.user.id)

    # Follow status map
    following_ids = set(
        Follow.objects.filter(follower=request.user)
                      .values_list('following_id', flat=True)
    )

    results = []
    for u in users:
        results.append({
            "user": u,
            "is_following": u.id in following_ids
        })

    return render(request, "search_results.html", {
        "results": results,
        "query": query,
    })