# Generated by Django 5.1 on 2024-09-05 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='rating',
            field=models.CharField(choices=[('ER', 'ER'), ('L', 'L'), ('AGE_10', 'AGE_10'), ('AGE_12', 'AGE_12'), ('AGE_14', 'AGE_14'), ('AGE_16', 'AGE_16'), ('AGE_18', 'AGE_18')], max_length=255),
        ),
    ]
