from django.db import models
from accounts.models import User
# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    price = models.PositiveIntegerField()
    image = models.FileField(upload_to='images', default='default_image.jpg')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="accounts")
