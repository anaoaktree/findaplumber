# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-02 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_auto_20160502_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='trader',
            name='page',
            field=models.TextField(default=b'', editable=False),
        ),
    ]
