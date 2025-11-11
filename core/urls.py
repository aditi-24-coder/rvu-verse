from django.urls import path
from . import views

urlpatterns = [
    # Authentication routes
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main routes
    path('', views.home_view, name='home'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    #changed by Shriyaa
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),  # ✅ New
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),  # ✅ New
    path('post/create/', views.create_post, name='create_post'),
    path('messages/', views.messages_view, name='messages'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('search/', views.search_view, name='search'),
    path('departments/', views.departments_view, name='departments'),
    
    # Event routes
    path('events/', views.events_view, name='events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    
    # AJAX routes for posts and users
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/unlike/', views.unlike_post, name='unlike_post'),
    path('user/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('user/<int:user_id>/unfollow/', views.unfollow_user, name='unfollow_user'),
    
    # AJAX routes for events
    path('events/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('events/<int:event_id>/cancel-registration/', views.cancel_event_registration, name='cancel_event_registration'),
    path('events/<int:event_id>/like/', views.like_event, name='like_event'),
    path('events/<int:event_id>/unlike/', views.unlike_event, name='unlike_event'),

    # added
    path('profile/<str:username>/', views.user_profile, name='profile'),

]
