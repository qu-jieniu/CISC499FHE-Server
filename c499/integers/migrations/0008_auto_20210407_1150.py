# Generated by Django 3.1.6 on 2021-04-07 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        ('integers', '0007_auto_20210330_1153'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Session',
            new_name='PersistentSession',
        ),
    ]
