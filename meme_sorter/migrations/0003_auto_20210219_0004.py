# Generated by Django 3.1 on 2021-02-18 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme_sorter', '0002_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='meme_warehaouse/'),
        ),
    ]
