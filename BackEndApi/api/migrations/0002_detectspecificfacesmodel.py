# Generated by Django 3.1.2 on 2020-10-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetectSpecificFacesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('targetName', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('targetImage', models.ImageField(blank=True, null=True, upload_to='images')),
            ],
        ),
    ]
