from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

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

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
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

def slug_generator(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(
        slug=slug
    ).order_by("-id")

    if qs.exists():
        new_slug = "%s-%s" %(slug, qs.first().id)
        return slug_generator(instance, new_slug=new_slug)
    return slug

def post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance)

pre_save.connect(post_receiver, sender=Post)
