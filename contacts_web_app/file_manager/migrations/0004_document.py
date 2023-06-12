# Generated by Django 4.2.2 on 2023-06-11 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0003_alter_library_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
