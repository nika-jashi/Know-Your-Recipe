# Generated by Django 4.2.6 on 2023-12-12 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
        ('recipes', '0005_alter_recipe_preparation_time_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='ingredients.ingredient'),
        ),
    ]
