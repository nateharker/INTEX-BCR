# Generated by Django 3.1.4 on 2020-12-08 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joblisting',
            name='description',
            field=models.CharField(max_length=9000),
        ),
    ]