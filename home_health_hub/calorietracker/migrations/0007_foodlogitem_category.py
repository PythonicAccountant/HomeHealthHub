# Generated by Django 3.2.10 on 2022-04-21 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calorietracker', '0006_alter_food_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodlogitem',
            name='category',
            field=models.CharField(choices=[('b', 'Breakfast'), ('l', 'Lunch'), ('d', 'Dinner'), ('s', 'Snack')], default='s', max_length=1),
        ),
    ]
