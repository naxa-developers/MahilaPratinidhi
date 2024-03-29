# Generated by Django 2.0.7 on 2019-01-02 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20181213_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='dob',
            field=models.CharField(blank=True, max_length=300, verbose_name='Date of Birth'),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='fathers_name',
            field=models.CharField(blank=True, max_length=300, verbose_name="Father's Name"),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='mothers_name',
            field=models.CharField(blank=True, max_length=300, verbose_name="Mother's Name"),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='name_of_elected_region',
            field=models.CharField(blank=True, max_length=300, verbose_name='Name.of.elected.region_NE'),
        ),
        migrations.AddField(
            model_name='mahilapratinidhiform',
            name='ward',
            field=models.CharField(blank=True, max_length=300, verbose_name='Ward'),
        ),
        migrations.AlterField(
            model_name='mahilapratinidhiform',
            name='age',
            field=models.CharField(max_length=300, verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='mahilapratinidhiform',
            name='age_en',
            field=models.CharField(max_length=300, null=True, verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='mahilapratinidhiform',
            name='age_ne_NP',
            field=models.CharField(max_length=300, null=True, verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='pratinidhishava',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='featured'),
        ),
        migrations.AlterField(
            model_name='pratinidhishava',
            name='hlcit_code',
            field=models.CharField(max_length=20, null=True, verbose_name='hlcit_code'),
        ),
        migrations.AlterField(
            model_name='pratinidhishava',
            name='husbands_name',
            field=models.CharField(blank=True, max_length=300, verbose_name='श्रीमानको नाम'),
        ),
        migrations.AlterField(
            model_name='pratinidhishava',
            name='husbands_name_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='श्रीमानको नाम'),
        ),
        migrations.AlterField(
            model_name='pratinidhishava',
            name='husbands_name_ne_NP',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='श्रीमानको नाम'),
        ),
        migrations.AlterField(
            model_name='provincemahilapratinidhiform',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='featured'),
        ),
        migrations.AlterField(
            model_name='provincemahilapratinidhiform',
            name='hlcit_code',
            field=models.CharField(max_length=20, null=True, verbose_name='hlcit_code'),
        ),
        migrations.AlterField(
            model_name='provincemahilapratinidhiform',
            name='husbands_name',
            field=models.CharField(blank=True, max_length=300, verbose_name='श्रीमानको नाम'),
        ),
        migrations.AlterField(
            model_name='provincemahilapratinidhiform',
            name='husbands_name_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='श्रीमानको नाम'),
        ),
        migrations.AlterField(
            model_name='provincemahilapratinidhiform',
            name='husbands_name_ne_NP',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='श्रीमानको नाम'),
        ),
        migrations.AlterField(
            model_name='rastriyashava',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='featured'),
        ),
        migrations.AlterField(
            model_name='rastriyashava',
            name='hlcit_code',
            field=models.CharField(max_length=20, null=True, verbose_name='hlcit_code'),
        ),
        migrations.AlterField(
            model_name='rastriyashava',
            name='husbands_name',
            field=models.CharField(blank=True, max_length=300, verbose_name='श्रीमानको नाम'),
        ),
        migrations.AlterField(
            model_name='rastriyashava',
            name='husbands_name_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='श्रीमानको नाम'),
        ),
        migrations.AlterField(
            model_name='rastriyashava',
            name='husbands_name_ne_NP',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='श्रीमानको नाम'),
        ),
    ]
