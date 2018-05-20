# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-20 02:03
from __future__ import unicode_literals

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.get_image_path),
        ),
    ]