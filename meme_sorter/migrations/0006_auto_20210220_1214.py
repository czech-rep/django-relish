# Generated by Django 3.1 on 2021-02-20 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme_sorter', '0005_auto_20210219_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='tags',
        ),
        migrations.AddField(
            model_name='image',
            name='tags',
            field=models.ManyToManyField(to='meme_sorter.TagName'),
        ),
    ]