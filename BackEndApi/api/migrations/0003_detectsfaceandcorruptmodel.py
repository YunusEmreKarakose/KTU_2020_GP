# Generated by Django 3.1.2 on 2020-10-27 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_detectspecificfacesmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetectSFaceAndCorruptModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('targetName', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('targetImage', models.ImageField(blank=True, null=True, upload_to='images')),
            ],
        ),
    ]
