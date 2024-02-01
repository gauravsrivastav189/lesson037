# Generated by Django 4.2.9 on 2024-01-31 11:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0005_book"),
    ]

    operations = [
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField()),
                ("name", models.CharField(max_length=30)),
                ("book", models.ManyToManyField(to="library.book")),
            ],
        ),
    ]
