from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class SavedData(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60, unique=True)
    data = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Update slug if title has changed or slug is not set
        if self.pk is None or self.title != SavedData.objects.get(pk=self.pk).title:
            self.slug = slugify(self.title)
        
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title}"
    
