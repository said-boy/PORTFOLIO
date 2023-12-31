# Generated by Django 4.2.4 on 2023-08-26 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=25, unique=True)),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/profiles/')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=25)),
                ('slug', models.SlugField()),
                ('stock', models.IntegerField()),
                ('price', models.IntegerField()),
                ('description', models.TextField(max_length=300)),
                ('image', models.ImageField(upload_to='images/products/')),
                ('created_at', models.DateField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riva_api.category', to_field='name')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riva_api.seller', to_field='name')),
            ],
            options={
                'ordering': ['slug'],
            },
        ),
    ]
