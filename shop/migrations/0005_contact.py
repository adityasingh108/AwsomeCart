# Generated by Django 3.2.3 on 2021-06-09 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20210605_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('desc', models.CharField(default='', max_length=1000)),
            ],
        ),
    ]
