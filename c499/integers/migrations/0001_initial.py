# Generated by Django 3.1.6 on 2021-03-03 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Int_Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('X', models.IntegerField(default=0)),
                ('q', models.IntegerField(default=0)),
            ],
        ),
    ]