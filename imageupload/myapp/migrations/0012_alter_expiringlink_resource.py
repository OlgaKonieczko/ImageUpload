# Generated by Django 4.2.6 on 2023-10-09 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0011_alter_expiringlink_resource"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expiringlink",
            name="resource",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="myapp.image"
            ),
        ),
    ]
