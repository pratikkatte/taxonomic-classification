# Generated by Django 2.2.7 on 2019-11-23 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_name', models.CharField(max_length=50)),
                ('model_name', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
