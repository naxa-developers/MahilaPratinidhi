# Generated by Django 2.0.7 on 2019-03-24 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190211_0510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='province',
        ),
    ]
