# Generated by Django 4.0 on 2022-01-15 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchengin_backend', '0007_jaccardgraph'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookm',
            name='rank',
            field=models.IntegerField(default='0'),
        ),
    ]