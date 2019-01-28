# Generated by Django 2.0.7 on 2019-01-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190102_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='fathers_name_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name="Father's Name"),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='fathers_name_ne_NP',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name="Father's Name"),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='mothers_name_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name="Mother's Name"),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='mothers_name_ne_NP',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name="Mother's Name"),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='name_of_elected_region_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Name.of.elected.region_NE'),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='name_of_elected_region_ne_NP',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Name.of.elected.region_NE'),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='prapta_maat_sankhya',
            field=models.CharField(blank=True, max_length=300, verbose_name='Votes'),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='prapta_maat_sankhya_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Votes'),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='prapta_maat_sankhya_ne_NP',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Votes'),
        ),
    ]
