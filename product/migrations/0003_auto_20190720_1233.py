# Generated by Django 2.2.1 on 2019-07-20 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20190720_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='status',
            field=models.IntegerField(choices=[(2, 'BLOCK'), (1, 'ACCEPT'), (0, 'REQUEST')], default=0),
        ),
    ]
