# Generated by Django 3.0 on 2020-03-21 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listapp', '0003_auto_20200319_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_counttype',
            field=models.CharField(choices=[('li', 'l'), ('kilo', 'kg'), ('piec', 'pc')], max_length=5),
        ),
    ]
