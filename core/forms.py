from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, Post, Comment, Message, Department, Event, EventComment, EventRegistration

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    
    class Meta:
        model = User
        fields = ['username', 'password']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'College Email'}),
        help_text='Required. Email must end with one of: btech22@rvu.edu.in, btech23@rvu.edu.in, or btech24@rvu.edu.in'
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        help_text='Required. Letters, digits and @/./+/-/_ only.'
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        help_text='Your password must be at least 8 characters long and not too common.'
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        help_text='Enter the same password as before, for verification.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        allowed_endings = ['btech22@rvu.edu.in', 'btech23@rvu.edu.in', 'btech24@rvu.edu.in']
        
        # Check if email ends with any of the allowed domain patterns
        if not any(email.endswith(ending) for ending in allowed_endings):
            raise ValidationError('Your email must end with one of: btech22@rvu.edu.in, btech23@rvu.edu.in, or btech24@rvu.edu.in')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with that email already exists.')
        
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'department', 'study_year']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'study_year': forms.Select(attrs={'class': 'form-control'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'department', 'hashtags', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What\'s on your mind?'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'hashtags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Separate hashtags with commas (e.g., events, announcement)'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Add a comment...'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Type your message...'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'department', 'location', 'start_date', 'end_date', 'hashtags', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Event Description'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Location'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'hashtags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Separate hashtags with commas (e.g., workshop, technical)'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EventEditForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'department', 'location', 'start_date', 'end_date', 'hashtags', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Event Description'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Location'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'hashtags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Separate hashtags with commas (e.g., workshop, technical)'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Add a comment...'}),
        }

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class SearchForm(forms.Form):
    SEARCH_CHOICES = [
        ('posts', 'Posts'),
        ('users', 'Users'),
        ('hashtags', 'Hashtags'),
        ('events', 'Events'),
    ]
    
    query = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search...'})
    )
    
    search_type = forms.ChoiceField(
        choices=SEARCH_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="All Departments"
    )
    
    study_year = forms.ChoiceField(
        choices=[('', 'All Years')] + Profile.YEAR_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
