from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator
#added
from django.contrib.auth.models import User
from .models import Follow

from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, ProfileForm, 
    PostForm, CommentForm, MessageForm, SearchForm, EventForm, EventEditForm,
    EventCommentForm, EventRegistrationForm
)
from .models import (
    Profile, Post, Comment, Like, Follow, Message, 
    Notification, Department, Event, EventComment, EventLike, 
    EventRegistration
)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}. You can now log in.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def home_view(request):
    # Get all posts sorted by creation time
    posts = Post.objects.all().select_related('user', 'department').prefetch_related('comments', 'likes')
    
    # Get user's liked posts
    user_likes = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    
    # Get departments for filtering
    departments = Department.objects.all()
    
    # Filter by department if specified
    department_id = request.GET.get('department')
    if department_id:
        posts = posts.filter(department_id=department_id)
    
    # Paginate posts
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Post form for creating new posts
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, "Your post has been created!")
            return redirect('home')
    else:
        post_form = PostForm()
    
    context = {
        'page_obj': page_obj,
        'post_form': post_form,
        'user_likes': user_likes,
        'departments': departments,
        'current_department': department_id,
    }
    
    return render(request, 'core/home.html', context)

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user).select_related('user', 'department')
    
    # Check if the current user follows this profile
    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()
    
    # Check if this profile follows the current user (for messaging)
    is_followed_by = Follow.objects.filter(
        follower=profile_user,
        following=request.user
    ).exists()
    
    # Can message only if both users follow each other
    can_message = is_following and is_followed_by
    
    # Get follow stats
    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    #added
    followers = profile_user.followers.all().select_related('follower')
    following = profile_user.following.all().select_related('following')
    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'is_followed_by': is_followed_by,
        'can_message': can_message,
        'followers_count': followers_count,
        'following_count': following_count,
        'followers': [f.follower for f in followers],
        'following': [f.following for f in following],
    }
    
    return render(request, 'core/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('user_profile', username=request.user.username)
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'core/edit_profile.html', {'profile_form': profile_form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).select_related('user')
    
    # Check if user has liked this post
    user_has_liked = Like.objects.filter(user=request.user, post=post).exists()
    
    # Handle comment form
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            # Create notification for post owner
            if request.user != post.user:
                Notification.objects.create(
                    user=post.user,
                    notification_type='comment',
                    from_user=request.user,
                    post=post,
                    comment=comment,
                    text=f"{request.user.username} commented on your post."
                )
            
            messages.success(request, "Comment added successfully!")
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
    }
    
    return render(request, 'core/post_detail.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Your post has been created!")
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'core/create_post.html', {'form': form})

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    # If this was a new like, create a notification
    if created and request.user != post.user:
        Notification.objects.create(
            user=post.user,
            notification_type='like',
            from_user=request.user,
            post=post,
            text=f"{request.user.username} liked your post."
        )
    
    likes_count = post.likes.count()
    return JsonResponse({'status': 'success', 'likes_count': likes_count})

@login_required
@require_POST
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Like.objects.filter(user=request.user, post=post).delete()
    likes_count = post.likes.count()
    return JsonResponse({'status': 'success', 'likes_count': likes_count})

@login_required
@require_POST
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    # Don't allow self-follow
    if request.user == user_to_follow:
        return JsonResponse({'status': 'error', 'message': 'You cannot follow yourself'})
    
    # Create follow relationship
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    
    # Create notification for the followed user
    if created:
        Notification.objects.create(
            user=user_to_follow,
            notification_type='follow',
            from_user=request.user,
            text=f"{request.user.username} started following you."
        )
    
    followers_count = Follow.objects.filter(following=user_to_follow).count()
    return JsonResponse({'status': 'success', 'followers_count': followers_count})

@login_required
@require_POST
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    
    # Delete the follow relationship
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    
    followers_count = Follow.objects.filter(following=user_to_unfollow).count()
    return JsonResponse({'status': 'success', 'followers_count': followers_count})

@login_required
def messages_view(request):
    # Get unique users who have conversations with the current user
    conversations = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()
    
    selected_user_id = request.GET.get('user')
    selected_user = None
    messages_with_user = []
    
    if selected_user_id:
        selected_user = get_object_or_404(User, id=selected_user_id)
        
        # Check if both users follow each other
        mutual_follow = Follow.objects.filter(
            follower=request.user, following=selected_user
        ).exists() and Follow.objects.filter(
            follower=selected_user, following=request.user
        ).exists()
        
        if not mutual_follow:
            messages.error(request, "You can only message users who follow you and whom you follow.")
            return redirect('messages_view')
        
        # Get messages between the two users
        messages_with_user = Message.objects.filter(
            (Q(sender=request.user, receiver=selected_user) | 
             Q(sender=selected_user, receiver=request.user))
        ).order_by('created_at')
        
        # Mark messages as read
        Message.objects.filter(sender=selected_user, receiver=request.user, is_read=False).update(is_read=True)
        
        # Handle new message form
        if request.method == 'POST':
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.sender = request.user
                message.receiver = selected_user
                message.save()
                
                # Create notification
                Notification.objects.create(
                    user=selected_user,
                    notification_type='message',
                    from_user=request.user,
                    message=message,
                    text=f"New message from {request.user.username}"
                )
                
                return redirect(f'/messages/?user={selected_user.id}')
        else:
            message_form = MessageForm()
    else:
        message_form = None
    
    context = {
        'conversations': conversations,
        'selected_user': selected_user,
        'messages_with_user': messages_with_user,
        'message_form': message_form,
    }
    
    return render(request, 'core/messages.html', context)
#changed by Shriyaa
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark all as read
    if request.GET.get('mark_all_read'):
        notifications.update(is_read=True)
        return redirect('notifications')
    
    # Mark single notification as read
    notification_id = request.GET.get('mark_read')
    if notification_id:
        Notification.objects.filter(id=notification_id, user=request.user).update(is_read=True)
        return redirect('notifications')
    
    # Paginate notifications
    paginator = Paginator(notifications, 20)  # Show 20 notifications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/notifications.html', {'page_obj': page_obj})

@login_required
def search_view(request):
    results = []
    search_performed = False
    
    if request.method == 'GET' and 'query' in request.GET:
        search_performed = True
        form = SearchForm(request.GET)
        
        if form.is_valid():
            query = form.cleaned_data.get('query')
            search_type = form.cleaned_data.get('search_type')
            department = form.cleaned_data.get('department')
            study_year = form.cleaned_data.get('study_year')
            
            if search_type == 'posts':
                # Search for posts
                results = Post.objects.filter(
                    Q(content__icontains=query) | Q(hashtags__icontains=query)
                ).select_related('user', 'department')
                
                # Apply department filter if specified
                if department:
                    results = results.filter(department=department)
                
            elif search_type == 'users':
                # Search for users
                results = User.objects.filter(
                    Q(username__icontains=query) | 
                    Q(first_name__icontains=query) | 
                    Q(last_name__icontains=query)
                ).select_related('profile')
                
                # Apply department filter if specified
                if department:
                    results = results.filter(profile__department=department)
                
                # Apply study year filter if specified
                if study_year:
                    results = results.filter(profile__study_year=study_year)
                
            elif search_type == 'hashtags':
                # Search for posts with specific hashtags
                results = Post.objects.filter(
                    hashtags__icontains=query
                ).select_related('user', 'department')
                
                # Apply department filter if specified
                if department:
                    results = results.filter(department=department)
                    
            elif search_type == 'events':
                # Search for events
                results = Event.objects.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(location__icontains=query) |
                    Q(hashtags__icontains=query)
                ).select_related('organizer', 'department')
                
                # Apply department filter if specified
                if department:
                    results = results.filter(department=department)
    else:
        form = SearchForm()
    
    context = {
        'form': form,
        'results': results,
        'search_performed': search_performed,
    }
    
    return render(request, 'core/search.html', context)

@login_required
def departments_view(request):
    departments = Department.objects.all().annotate(
        post_count=Count('posts')
    )
    
    selected_department_id = request.GET.get('department')
    posts = None
    
    if selected_department_id:
        selected_department = get_object_or_404(Department, id=selected_department_id)
        posts = Post.objects.filter(department=selected_department).select_related('user')
        
        # Paginate department posts
        paginator = Paginator(posts, 10)  # Show 10 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'departments': departments,
            'selected_department': selected_department,
            'page_obj': page_obj,
        }
    else:
        context = {
            'departments': departments,
        }
    
    return render(request, 'core/departments.html', context)

@login_required
def events_view(request):
    # Get all events
    events = Event.objects.all().select_related('organizer', 'department')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        events = events.filter(status=status)
    
    # Filter by department
    department_id = request.GET.get('department')
    if department_id:
        events = events.filter(department_id=department_id)
    
    # Get all departments for filtering
    departments = Department.objects.all()
    
    # Paginate events
    paginator = Paginator(events, 9)  # Show 9 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'departments': departments,
        'current_department': department_id,
        'current_status': status,
        'status_choices': Event.STATUS_CHOICES,
    }
    
    return render(request, 'core/events.html', context)

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            
            messages.success(request, "Your event has been created!")
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    
    return render(request, 'core/create_event.html', {'form': form})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    comments = EventComment.objects.filter(event=event).select_related('user')
    
    # Check if user is registered for this event
    is_registered = EventRegistration.objects.filter(
        user=request.user, 
        event=event
    ).exists() if request.user.is_authenticated else False
    
    # Check if user has liked this event
    user_has_liked = EventLike.objects.filter(
        user=request.user, 
        event=event
    ).exists() if request.user.is_authenticated else False
    
    # Handle comment form
    if request.method == 'POST':
        comment_form = EventCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.event = event
            comment.save()
            
            # Create notification for event organizer
            if request.user != event.organizer:
                Notification.objects.create(
                    user=event.organizer,
                    notification_type='comment',
                    from_user=request.user,
                    event=event,
                    text=f"{request.user.username} commented on your event '{event.title}'."
                )
            
            messages.success(request, "Comment added successfully!")
            return redirect('event_detail', event_id=event.id)
    else:
        comment_form = EventCommentForm()
    
    context = {
        'event': event,
        'comments': comments,
        'comment_form': comment_form,
        'is_registered': is_registered,
        'user_has_liked': user_has_liked,
    }
    
    return render(request, 'core/event_detail.html', context)

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is the organizer of this event
    if request.user != event.organizer:
        messages.error(request, "You don't have permission to edit this event.")
        return redirect('event_detail', event_id=event.id)
    
    if request.method == 'POST':
        form = EventEditForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventEditForm(instance=event)
    
    return render(request, 'core/edit_event.html', {'form': form, 'event': event})

@login_required
@require_POST
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Don't allow registration for past events
    if event.is_past_event():
        return JsonResponse({'status': 'error', 'message': 'Cannot register for past events'})
    
    # Create registration
    registration, created = EventRegistration.objects.get_or_create(
        user=request.user,
        event=event,
        defaults={'status': 'registered'}
    )
    
    if created:
        # Create notification for event organizer
        Notification.objects.create(
            user=event.organizer,
            notification_type='event_registration',
            from_user=request.user,
            event=event,
            text=f"{request.user.username} registered for your event '{event.title}'."
        )
    
    registrations_count = event.registrations.count()
    return JsonResponse({'status': 'success', 'registrations_count': registrations_count})

@login_required
@require_POST
def cancel_event_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    EventRegistration.objects.filter(user=request.user, event=event).delete()
    
    registrations_count = event.registrations.count()
    return JsonResponse({'status': 'success', 'registrations_count': registrations_count})

@login_required
@require_POST
def like_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    like, created = EventLike.objects.get_or_create(user=request.user, event=event)
    
    # If this was a new like, create a notification
    if created and request.user != event.organizer:
        Notification.objects.create(
            user=event.organizer,
            notification_type='like',
            from_user=request.user,
            event=event,
            text=f"{request.user.username} liked your event '{event.title}'."
        )
    
    likes_count = event.event_likes.count()
    return JsonResponse({'status': 'success', 'likes_count': likes_count})

@login_required
@require_POST
def unlike_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    EventLike.objects.filter(user=request.user, event=event).delete()
    
    likes_count = event.event_likes.count()
    return JsonResponse({'status': 'success', 'likes_count': likes_count})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('profile', username=request.user.username)
    
    return redirect('profile', username=request.user.username)
#changed by Shriyaa
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'core/edit_post.html', {'form': form, 'post': post})

