from django.db import models
from django.core.files import File
from io import BytesIO
from PIL import Image
import os
from django.conf import settings


def update_image_name(instance, filename):
        path = "uploads/images/"
        name = instance.slug + os.path.splitext(filename)[1]
        return os.path.join(path, name)

def update_thumbnail_name(instance, filename):
        path = "uploads/thumbnails/"
        name = instance.slug + os.path.splitext(filename)[1]
        return os.path.join(path, name)

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return f'/{self.slug}'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to=update_image_name, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=update_thumbnail_name, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)  

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}'
    
    def get_image(self):
        if self.image:
            return settings.BASE_URL + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return settings.BASE_URL + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return settings.BASE_URL + self.thumbnail.url
            else:
                return ''
            
    def get_image_name(self):
        return os.path.basename(self.image.name)
            
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=self.get_image_name())
        return thumbnail
    