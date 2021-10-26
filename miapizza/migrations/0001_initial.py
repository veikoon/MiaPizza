# Generated by Django 2.1.2 on 2018-10-18 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('last_update', models.DateTimeField(verbose_name='Dernier mouvement sur les ingredients')),
                ('quentity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ingredients', models.CharField(max_length=500)),
                ('last_update', models.DateTimeField(verbose_name='Dernier mouvement sur les pizzas')),
            ],
        ),
    ]