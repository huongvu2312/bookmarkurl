from django.db import models
from django.conf import settings


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='categorys', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
        unique_together = (('name', 'user'),)

    def __str__(self):
        return f'#{self.user.id}  {self.user} - {self.name}'

    def get_absolute_url(self):
        return f'category/{self.slug}/'


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='bookmarks', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name='bookmarks', on_delete=models.CASCADE)
    url = models.CharField(max_length=255, unique=True)
    copy = models.PositiveIntegerField(null=True, default=0)
    note = models.CharField(blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return f'bookmark/{self.id}/'
