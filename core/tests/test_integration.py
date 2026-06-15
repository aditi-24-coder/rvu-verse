from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Post, Follow, Message, Department

class RVUverseIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a department for registration and posts
        self.dept = Department.objects.create(code='5', name='SOCSE')
        
        # We will create a test user manually to bypass the complex form validation for this simple test
        self.user1 = User.objects.create_user(username='testuser1', email='testuser1@rvu.edu.in', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', email='testuser2@rvu.edu.in', password='password123')

    def test_login_and_create_post_flow(self):
        """Test that a user can login, create a post, and see it on the home feed."""
        # 1. Login
        response = self.client.post(reverse('login'), {
            'username': 'testuser1',
            'password': 'password123'
        })
        # Should redirect to home after login
        self.assertRedirects(response, reverse('home'))
        
        # 2. Create a Post
        response = self.client.post(reverse('home'), {
            'content': 'Integration test post content',
            'department': self.dept.id,
            'hashtags': 'test,integration'
        })
        self.assertRedirects(response, reverse('home'))
        
        # Verify the post is in the database
        self.assertTrue(Post.objects.filter(content='Integration test post content', user=self.user1).exists())
        
        # 3. View the Home Feed
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Integration test post content')
        self.assertContains(response, '#test')
        self.assertContains(response, '#integration')

    def test_mutual_follow_and_messaging_flow(self):
        """Test that users can follow each other and send messages."""
        # 1. Login user 1
        self.client.login(username='testuser1', password='password123')
        
        # User 1 follows User 2
        response = self.client.post(reverse('follow_user', args=[self.user2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())
        
        # User 1 tries to send a message to User 2 (should fail because not mutual yet)
        response = self.client.get(reverse('messages') + f'?user={self.user2.id}')
        # Should redirect back to messages base because of error message "You can only message users who follow you..."
        self.assertRedirects(response, reverse('messages'))
        
        # 2. Login user 2
        self.client.login(username='testuser2', password='password123')
        
        # User 2 follows User 1
        response = self.client.post(reverse('follow_user', args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)
        
        # 3. User 2 sends a message to User 1
        response = self.client.post(reverse('messages') + f'?user={self.user1.id}', {
            'content': 'Hello User 1! This is an integration test.'
        })
        # Should redirect to the conversation
        self.assertRedirects(response, f"/messages/?user={self.user1.id}")
        
        # Verify message is in the DB
        self.assertTrue(Message.objects.filter(sender=self.user2, receiver=self.user1, content='Hello User 1! This is an integration test.').exists())
