# Generated by Django 3.0.6 on 2025-04-03 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'product_master',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='VariantMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'variant_master',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='VariantOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variant_master_name', to='product_app.VariantMaster')),
            ],
            options={
                'db_table': 'variant_option',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProductOverallQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.IntegerField()),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_master_name', to='product_app.ProductMaster')),
                ('variant_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant_option_product_name', to='product_app.VariantOption')),
            ],
            options={
                'db_table': 'product_overall_quantity',
                'ordering': ('created_at',),
            },
        ),
    ]
