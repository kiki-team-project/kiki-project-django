from django.db import models
from django.conf import settings

class Post(models.Model):
    nickname = models.CharField(max_length=200)  # 제목
    category = models.CharField(max_length=200) 
    platform = models.CharField(max_length=50) 
    content = models.TextField()  # 내용
    author = models.EmailField(
        max_length=255,
    )
    like_post = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 일시
    updated_at = models.DateTimeField(auto_now=True)  # 수정 일시

    def __str__(self):
        return self.nickname

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # 해당 댓글이 속한 게시글
    author = models.EmailField(
        max_length=255,
    )
    like_post = models.IntegerField()
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 일시

    def __str__(self):
        return f'{self.author} - {self.content}'
    
    
class CategoryList(models.Model):
    category = models.CharField(max_length=50) 
    
    def __str__(self):
        return self.category

class PlatformList(models.Model):
    platform = models.CharField(max_length=50) 

    def __str__(self):
        return self.platform

