# Generated by Django 3.2.3 on 2021-08-11 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_alter_orderupdate_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateField(default=''),
        ),
    ]
