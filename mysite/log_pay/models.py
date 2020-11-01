#-*- coding: utf-8 -*-
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from django.conf import settings
from datetime import datetime

# Create your models here.
private_storage = FileSystemStorage(location=settings.PRIVATE_STORAGE_ROOT)
media_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

#Class's doc
class Type(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Название класса')
    example = models.FileField('Образец', storage=private_storage)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

class Doc(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Название документа')
    file = models.CharField(max_length = 580, verbose_name='Ссылка документа')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, verbose_name='Класс документа', related_name='doc')
    nomber = models.CharField(max_length = 128, verbose_name='Номер документа')
    year = models.IntegerField(default=0, verbose_name='Год')
    adress = models.CharField(max_length = 128, verbose_name='Адрес')
    owner = models.CharField(max_length = 128, verbose_name='Владелец')
    lat = models.FloatField(default=0, verbose_name='Широта, °')
    long = models.FloatField(default=0, verbose_name='Долгота, °')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
