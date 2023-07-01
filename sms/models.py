from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Create your models here.

class Category(models.Model):
    cat_title=models.CharField(max_length=200)


    def __str__(self):
        return self.cat_title
    

class Post(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    image=models.ImageField(upload_to="post/")
    slug=models.CharField(max_length=200, unique=True)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_post')
    def __str__(self):
        return self.title
  
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):  # new
     if not self.slug:
         self.slug = slugify(self.title)
     return super().save(*args, **kwargs)    

    