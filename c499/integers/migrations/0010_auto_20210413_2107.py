# Generated by Django 3.1.6 on 2021-04-14 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integers', '0009_auto_20210408_0923'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='integer',
            options={'ordering': ['set_id', 'index']},
        ),
        migrations.AlterField(
            model_name='integer',
            name='X',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='integer',
            name='q',
            field=models.BinaryField(),
        ),
    ]