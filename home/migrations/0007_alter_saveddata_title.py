# Generated by Django 4.2.6 on 2024-03-09 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_saveddata_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saveddata',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]
