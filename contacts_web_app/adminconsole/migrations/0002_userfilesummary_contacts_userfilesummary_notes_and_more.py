# Generated by Django 4.2.2 on 2023-06-21 12:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("adminconsole", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userfilesummary",
            name="contacts",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="userfilesummary",
            name="notes",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="userfilesummary",
            name="summary_files",
            field=models.IntegerField(default=0),
        ),
    ]
