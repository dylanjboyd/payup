# Generated by Django 2.2.4 on 2019-08-10 03:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordshare',
            name='share',
            field=models.PositiveSmallIntegerField(default=10, validators=[django.core.validators.MinValueValidator(0),
                                                                           django.core.validators.MaxValueValidator(
                                                                               100)]),
            preserve_default=False,
        ),
    ]
