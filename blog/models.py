from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

from PIL import Image

class Category(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.title


class Article(models.Model):
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    pub_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default_image.jpg', upload_to='article_pics')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kawrgs):
        super().save(*args, **kawrgs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.name, self.content[:20])