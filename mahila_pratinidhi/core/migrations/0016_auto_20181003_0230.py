# Generated by Django 2.0.7 on 2018-10-03 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20180927_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provincemahilapratinidhiform',
            name='updated_marital_status',
        ),
        migrations.AlterField(
            model_name='provincemahilapratinidhiform',
            name='aaja_vanda_agadi_chunab_ladnu_vayeko_chha',
            field=models.CharField(choices=[('समानुपातिक', 'समानुपातिक'), ('छैन', 'छैन'), ('छ', 'छ')], max_length=300, verbose_name='आज भन्दा अघि चुनाब लड्नुभएको छ?'),
        ),
        migrations.AlterField(
            model_name='provincemahilapratinidhiform',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('cljjflxt', 'अविवाहित'), ('ljjflxt', 'विवाहित'), ('Psn', 'एकल'), ('cGo', 'अन्य')], max_length=300, null=True, verbose_name='बैवाहिक स्थिथि'),
        ),
        migrations.AlterField(
            model_name='provincemahilapratinidhiform',
            name='nirwachit_padh',
            field=models.CharField(blank=True, choices=[('सांसद - प्रदेशसभा', 'सांसद - प्रदेशसभा')], max_length=300, verbose_name='निर्वाचित पद'),
        ),
        migrations.AlterField(
            model_name='provincemahilapratinidhiform',
            name='nirwachit_prakriya',
            field=models.CharField(blank=True, choices=[('समानुपातिक', 'समानुपातिक'), ('प्रतक्ष्य', 'प्रतक्ष्य')], max_length=300, verbose_name='निर्वाचित प्रक्रिया'),
        ),
        migrations.AlterField(
            model_name='provincemahilapratinidhiform',
            name='nirwachit_vayeko_chhetra_aafno_thegana',
            field=models.CharField(blank=True, choices=[('हो', 'हो'), ('होइन', 'होइन')], max_length=300, null=True, verbose_name='निर्वाचित भएको क्षेत्र आफ्नो अस्थायी/ स्थायी ठेगाना भन्दा फरक'),
        ),
        migrations.AlterField(
            model_name='provincemahilapratinidhiform',
            name='pichidiyeko_chhetra_ho_hoina',
            field=models.CharField(blank=True, choices=[('हो', 'हो'), ('होइन', 'होइन')], max_length=300, verbose_name='पिछडिएको क्षेत्र हो कि होइन'),
        ),
    ]
