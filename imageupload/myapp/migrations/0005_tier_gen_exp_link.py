# Generated by Django 4.2.6 on 2023-10-08 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_remove_size_tier_tier_sizes"),
    ]

    operations = [
        migrations.AddField(
            model_name="tier",
            name="gen_exp_link",
            field=models.BooleanField(default=False),
        ),
    ]