from datetime import date

from django.db import models
from django.conf import settings


class BinaryFile(models.Model):
    file = models.FileField(upload_to='uploads/binary/')
    added = models.DateField(auto_now_add = True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.file.name
    
    class Meta:
        verbose_name = 'Binary file'
        verbose_name_plural = 'Binary files'


class ImgFile(models.Model):
    file = models.ImageField(upload_to='uploads/images/')
    parent_file = models.ForeignKey(BinaryFile, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
    
    class Meta:
        verbose_name = 'Img file'
        verbose_name_plural = 'Img files'
        
