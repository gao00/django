# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20180305_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uaddress',
            field=models.CharField(default=b'\xe6\x97\xa0', max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uphone',
            field=models.CharField(default=b'\xe6\x97\xa0', max_length=11),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='ureceiver',
            field=models.CharField(default=b'\xe6\x97\xa0', max_length=20),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uyoubian',
            field=models.CharField(default=b'\xe6\x97\xa0', max_length=6),
        ),
    ]
