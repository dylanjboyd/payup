# Generated by Django 2.2.4 on 2019-08-09 01:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0002_auto_20190809_0043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountholder',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='bankrecord',
            options={'ordering': ['-unique_id']},
        ),
    ]