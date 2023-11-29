# Generated by Django 4.2.2 on 2023-11-28 20:55

import django.core.files.storage
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_release_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(storage=django.core.files.storage.FileSystemStorage(), upload_to='')),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
    ]
