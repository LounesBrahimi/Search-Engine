# Generated by Django 4.0 on 2022-01-03 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchengin_backend', '0002_alter_bookm_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookm',
            name='author',
            field=models.CharField(default='unknown', max_length=30),
        ),
    ]