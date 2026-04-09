import pytest
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from core.models import Post  # adjust app name accordingly

@pytest.mark.django_db
def test_post_creation_with_image():
    user = User.objects.create_user(username='imguser', password='password')
    
    # Create a temp image
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file, format='JPEG')
    tmp_file.seek(0)

    uploaded = SimpleUploadedFile('test.jpg', tmp_file.read(), content_type='image/jpeg')
    post = Post.objects.create(user=user, content="Post with image", image=uploaded)
    
    assert post.image is not None
    assert post.content == "Post with image"
