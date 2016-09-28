# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('freieit', '0002_auto_20160315_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expertprofile',
            name='available',
            field=models.BooleanField(default=False, help_text='disable eg if you are on holidays'),
        ),
        migrations.AlterField(
            model_name='expertprofile',
            name='charges',
            field=models.DecimalField(null=True, blank=True, max_digits=5, verbose_name='charges', help_text='per hour incl. VAT, leave blank if variable', decimal_places=2),
        ),
        migrations.AlterField(
            model_name='expertprofile',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='expert_images', verbose_name='image'),
        ),
    ]
