# Generated by Django 4.2.4 on 2023-09-04 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('riva_api', '0010_alter_inventory_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='seller',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventorys', related_query_name='inventorys', to='riva_api.seller', to_field='name'),
        ),
    ]
