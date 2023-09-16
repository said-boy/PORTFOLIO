# Generated by Django 4.2.4 on 2023-08-31 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('riva_api', '0002_alter_inventory_category_alter_inventory_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='username',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='seller',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]