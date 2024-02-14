from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    activate_code = models.CharField(max_length=64, blank=False, default=None)
    is_email_active = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_image:
            img = Image.open(self.profile_image.path) # Open image

            # resize image
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size) # Resize image
                img.save(self.profile_image.path) # Save it again and override the larger image
