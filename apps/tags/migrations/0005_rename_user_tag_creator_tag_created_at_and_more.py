# Generated by Django 4.2.6 on 2023-11-22 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0004_remove_tag_recipe_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='user',
            new_name='creator',
        ),
        migrations.AddField(
            model_name='tag',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2023-03-08 09:58:47'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
