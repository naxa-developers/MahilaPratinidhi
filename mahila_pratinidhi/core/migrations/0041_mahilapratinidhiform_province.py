# Generated by Django 2.0.7 on 2018-11-26 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20181126_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='province',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Province', verbose_name='प्रदेश'),
        ),
    ]