# Generated by Django 2.0.4 on 2018-05-04 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('sigla', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
    ]