# Generated by Django 4.2.3 on 2023-08-08 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0002_product_desc_product_img_alter_customer_ph_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
    ]