# Generated by Django 4.1 on 2022-09-21 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_alter_category_photo_alter_product_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='category_id',
            new_name='category',
        ),
    ]