# Generated by Django 5.1.6 on 2025-02-15 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0004_alter_entry_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='text',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='topic',
            name='text',
            field=models.CharField(max_length=20),
        ),
    ]
