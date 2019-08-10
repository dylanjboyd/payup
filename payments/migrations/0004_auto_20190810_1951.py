# Generated by Django 2.2.4 on 2019-08-10 07:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0003_accountholder_rounding_likelihood'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountholder',
            name='rounding_likelihood',
        ),
        migrations.AddField(
            model_name='accountholder',
            name='rounding_victim',
            field=models.BooleanField(default=False),
        ),
    ]