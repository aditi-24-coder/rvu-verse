from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

class Department(models.Model):
    DEPT_CHOICES = [
        ('1', 'School of Liberal Arts and Sciences (SOLAS)'),
        ('2', 'School of Design and Innovation (SODI)'),
        ('3', 'School of Business (SOB)'),
        ('4', 'School of Economics and Public Policy (SOEPP)'),
        ('5', 'School of Computer Science and Engineering (SOCSE)'),
        ('6', 'School of Law (SOL)'),
        ('7', 'School of Film, Media and Creative Arts (SOFMCA)'),
        ('8', 'School of Continuing Education & Professional Studies (SOCEPS)'),
        ('9', 'School of Allied and Healthcare Professions (SOAHP)'),
    ]

    code = models.CharField(max_length=2, choices=DEPT_CHOICES, unique=True,default='5')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]

    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,related_name='profile')
    study_year = models.CharField(max_length=10, choices=YEAR_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.user.username)])

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashtags = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def get_likes_count(self):
        return self.likes.count()

    def get_comments_count(self):
        return self.comments.count()

    def extract_hashtags(self):
        if not self.hashtags:
            return []
        return [tag.strip() for tag in self.hashtags.split(',') if tag.strip()]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"Like by {self.user.username} on post {self.post.id}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

class Event(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    hashtags = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_date']
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('event_detail', args=[str(self.id)])
        
    def get_likes_count(self):
        return self.event_likes.count()
        
    def get_comments_count(self):
        return self.event_comments.count()
        
    def get_registrations_count(self):
        return self.registrations.count()
        
    def extract_hashtags(self):
        if not self.hashtags:
            return []
        return [tag.strip() for tag in self.hashtags.split(',') if tag.strip()]
        
    def is_past_event(self):
        return self.end_date < timezone.now()
        
    def is_ongoing_event(self):
        now = timezone.now()
        return self.start_date <= now and self.end_date >= now

class EventComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_comments')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on event {self.event.title}"

class EventLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_likes')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'event')
    
    def __str__(self):
        return f"Like by {self.user.username} on event {self.event.title}"

class EventRegistration(models.Model):
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registration_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'event')
        
    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('message', 'Message'),
        ('event', 'Event'),
        ('event_registration', 'Event Registration'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.text}"
