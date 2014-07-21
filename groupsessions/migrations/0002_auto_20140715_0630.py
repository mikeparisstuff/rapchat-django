# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupsessions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupsession',
            name='beat',
            field=models.ForeignKey(default=1, to='groupsessions.Beat'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='clip',
            name='beat',
        ),
    ]
