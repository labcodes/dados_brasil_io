# Generated by Django 2.0.4 on 2018-05-07 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comum', '0001_initial'),
        ('empresas', '0004_auto_20180507_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='uf',
            field=models.ForeignKey(default='ND', on_delete=django.db.models.deletion.PROTECT, related_name='empresas', to='comum.Estado'),
            preserve_default=False,
        ),
    ]
