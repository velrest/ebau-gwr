# Generated by Django 2.2.14 on 2021-02-22 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("linker", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(name="gwrlink", options={"ordering": ["-id"]},),
    ]