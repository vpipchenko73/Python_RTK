# Generated by Django 4.2.6 on 2023-12-26 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_account_account_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, upload_to='article_images/', verbose_name='Иллюстрации'),
        ),
    ]
