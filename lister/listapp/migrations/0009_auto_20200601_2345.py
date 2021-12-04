# Generated by Django 3.0 on 2020-06-01 20:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('listapp', '0008_auto_20200326_0257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_value', models.CharField(default=None, max_length=8)),
                ('code_email', models.EmailField(default=None, max_length=254)),
                ('code_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('code_token', models.CharField(default=None, max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='item_type',
            field=models.CharField(choices=[('art and music', 'art and music'), ('books and stationery', 'books and stationery'), ('clothes and shoes', 'clothes and shoes'), ('cosmetics and beauty', 'cosmetics and beauty'), ('education', 'education'), ('electronics and devices', 'electronics and devices'), ('food and drink', 'food and drink'), ('health and medicine', 'health and medicine'), ('household products', 'household products'), ('repair', 'repair'), ('services', 'services'), ('other', 'other')], max_length=50),
        ),
    ]
