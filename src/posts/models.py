from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(
        max_length=120,
    )

    content = models.TextField()

    image = models.ImageField(
        blank=True,
        null=True,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return "/%s/" %(self.id)
        return reverse("posts:detail", kwargs={
            "id": self.id
        })

    class Meta:
        ordering = [
            "-timestamp", 
            "-updated"
        ] 