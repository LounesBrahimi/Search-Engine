# Generated by Django 4.0 on 2022-01-17 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchengin_backend', '0011_alter_bookm_author_alter_bookm_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookm',
            name='author',
            field=models.CharField(default='unknown', max_length=500),
        ),
        migrations.AlterField(
            model_name='bookm',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]