# Generated by Django 3.2.3 on 2021-06-01 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('put_in_good_hands_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.IntegerField(choices=[(0, 'fundacja'), (1, 'organizacja pozarządowa'), (2, 'zbiórka lokalna')], default=0),
        ),
    ]