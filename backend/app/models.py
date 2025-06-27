from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(default="")


class Book(models.Model):
    name = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
