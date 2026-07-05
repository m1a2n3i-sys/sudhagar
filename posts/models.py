from django.db import models
from django.contrib.auth.models import User


def post_image_upload_path(instance, filename):
    """
    Builds the path where an uploaded image is stored:
    media/post_images/<user_id>/<filename>
    Keeping each user's uploads in their own folder avoids filename clashes.
    """
    return f'post_images/{instance.author.id}/{filename}'


class Post(models.Model):
    # Every post belongs to exactly one user (the author).
    # on_delete=CASCADE means: if the user account is deleted, delete their posts too.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    title = models.CharField(max_length=150)
    caption = models.TextField(max_length=2200, blank=True)

    # ImageField needs Pillow installed. Images are saved inside MEDIA_ROOT.
    image = models.ImageField(upload_to=post_image_upload_path)

    created_at = models.DateTimeField(auto_now_add=True)  # set once, on creation
    updated_at = models.DateTimeField(auto_now=True)      # updated every save()

    class Meta:
        ordering = ['-created_at']  # newest posts first, everywhere by default

    def __str__(self):
        return f'{self.title} by {self.author.username}'
