# Generated by Django 2.2.1 on 2019-07-20 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20190720_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='status',
            field=models.IntegerField(choices=[(0, 'REQUEST'), (2, 'BLOCK'), (1, 'ACCEPT')], default=0),
        ),
    ]
