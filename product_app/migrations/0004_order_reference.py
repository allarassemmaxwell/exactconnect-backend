# Generated by Django 5.2 on 2025-04-08 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0003_orderitem_created_at_orderitem_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='reference',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
