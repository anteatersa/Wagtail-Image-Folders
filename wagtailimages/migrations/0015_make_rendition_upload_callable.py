# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailimages.models


class Migration(migrations.Migration):

    dependencies = [
        #('wagtailimages', '0012_copy_image_permissions_to_collections'),
        ('wagtailimages', '0014_auto_20160525_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rendition',
            name='file',
            field=models.ImageField(upload_to=wagtail.wagtailimages.models.get_rendition_upload_to, width_field='width', height_field='height'),
        ),
    ]
