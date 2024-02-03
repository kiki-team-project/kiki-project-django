from django.db import models

class ProgramList(models.Model):

    platform = models.CharField(max_length=100, verbose_name="플렛폼")
    image = models.ImageField(upload_to='images/') 
    #image = models.TextField(verbose_name="로고 이미지")
    
    def __str__(self):
        return self.platform
    
class ShortcutKey(models.Model):
    category = models.CharField(max_length=100, verbose_name="카테고리")
    keys = models.CharField(max_length=100, verbose_name="키 조합")
    description = models.TextField(verbose_name="설명")
    platform = models.CharField(max_length=100, verbose_name="플렛폼")
    index = models.IntegerField()
    bookmark = models.IntegerField()
    image = models.ImageField(upload_to='images/') 

    class Meta:
        ordering = ['-bookmark', '-index']  # 내림차순 정렬
        
    def __str__(self):
        return f"{self.keys.replace(' ', '+')}({self.platform})"