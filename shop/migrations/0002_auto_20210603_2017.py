# Generated by Django 3.2.3 on 2021-06-03 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_catogory',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(default='', upload_to='shop/images'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='product_sub_catogory',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='publish_date',
            field=models.DateField(default=''),
        ),
    ]