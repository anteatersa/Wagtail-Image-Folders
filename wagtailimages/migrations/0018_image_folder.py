# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0017_reduce_focal_point_key_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFolder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at', db_index=True)),
                ('path', models.TextField(blank=True)),
                ('folder', models.ForeignKey(to='wagtailimages.ImageFolder', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='folder',
            field=models.ForeignKey(to='wagtailimages.ImageFolder', blank=True, null=True),
        ),
    ]
