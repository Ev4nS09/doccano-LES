# Generated by Django 4.2.15 on 2025-03-30 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("perspective_types", "0001_initial"),
        ("perspectives", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="boundingboxperspective",
            name="item",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="perspective_types.perspectiveitem"
            ),
        ),
        migrations.AddField(
            model_name="categoryperspective",
            name="item",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="perspective_types.perspectiveitem"
            ),
        ),
        migrations.AddField(
            model_name="segmentationperspective",
            name="item",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="perspective_types.perspectiveitem"
            ),
        ),
        migrations.AddField(
            model_name="spanperspective",
            name="item",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="perspective_types.perspectiveitem"
            ),
        ),
    ]
