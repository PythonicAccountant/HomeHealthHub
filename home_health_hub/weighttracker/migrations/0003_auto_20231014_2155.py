# Generated by Django 3.2.13 on 2023-10-15 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weighttracker', '0002_weightlog_trend'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weightlog',
            options={'get_latest_by': 'date'},
        ),
        migrations.AddField(
            model_name='weightprofile',
            name='estimated_tdee',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weightprofile',
            name='height',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='weightlog',
            name='trend',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='weightlog',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True),
        ),
    ]