# Generated by Django 3.1.6 on 2021-05-23 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_myfacedetection'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebCamFD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b64image', models.TextField()),
            ],
        ),
    ]
