# Generated by Django 4.0.4 on 2024-02-15 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_emailmessage_sendto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='sendto',
            field=models.EmailField(max_length=254),
        ),
    ]