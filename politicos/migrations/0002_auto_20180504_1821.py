# Generated by Django 2.0.4 on 2018-05-04 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('politicos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partido',
            name='id',
        ),
        migrations.AlterField(
            model_name='partido',
            name='sigla',
            field=models.CharField(max_length=15, primary_key=True, serialize=False),
        ),
    ]
