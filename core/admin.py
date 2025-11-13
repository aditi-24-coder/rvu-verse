from django.contrib import admin
from .models import Profile, Post, Comment, Like, Follow, Message, Notification, Department, Event, EventComment, EventLike, EventRegistration

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'study_year', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio')
    list_filter = ('department', 'study_year')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'created_at')
    search_fields = ('content', 'user__username')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'content', 'created_at')
    search_fields = ('content', 'user__username')
    list_filter = ('created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    list_filter = ('created_at',)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'created_at')
    list_filter = ('created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'created_at', 'is_read')
    search_fields = ('content', 'sender__username', 'receiver__username')
    list_filter = ('created_at', 'is_read')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notification_type', 'created_at', 'is_read')
    search_fields = ('user__username',)
    list_filter = ('notification_type', 'created_at', 'is_read')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'organizer', 'department', 'location', 'start_date', 'end_date', 'status')
    search_fields = ('title', 'description', 'location', 'organizer__username')
    list_filter = ('status', 'department', 'start_date')
    date_hierarchy = 'start_date'

@admin.register(EventComment)
class EventCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'content', 'created_at')
    search_fields = ('content', 'user__username', 'event__title')
    list_filter = ('created_at',)

@admin.register(EventLike)
class EventLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'created_at')
    list_filter = ('created_at',)

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'status', 'registration_date')
    search_fields = ('user__username', 'event__title')
    list_filter = ('status', 'registration_date')
