from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
# Create your models here.


class category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class discussion(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='discussions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_discussions' , blank=True, null=True)
    author2 = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    img = models.ImageField(upload_to='discussion_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    

    def discussions_comments_count(self):
        return self.comments.aggregate(count=Count('id'))['count']
    class Meta:
        verbose_name_plural = 'Discussions'
        ordering = ['-created_at']



class comment(models.Model):
    discussion = models.ForeignKey(discussion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', blank=True, null=True)
    author2 = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username if self.author else self.author2} on {self.discussion.title}'
    class Meta:
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']
