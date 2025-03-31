# Generated by Django 4.2.15 on 2025-03-29 23:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("examples", "0008_assignment"),
        ("perspective_types", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SpanPerspective",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("start_offset", models.IntegerField()),
                ("end_offset", models.IntegerField()),
                (
                    "example",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="span", to="examples.example"
                    ),
                ),
                (
                    "perspective",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="perspective_types.spantype"),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="SegmentationPerspective",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("points", models.JSONField(default=list)),
                (
                    "example",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="segmentation", to="examples.example"
                    ),
                ),
                (
                    "perspective",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="perspective_types.categorytype"),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RelationPerspective",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "example",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="relation", to="examples.example"
                    ),
                ),
                (
                    "from_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="from_relations",
                        to="perspectives.spanperspective",
                    ),
                ),
                (
                    "to_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="to_relations",
                        to="perspectives.spanperspective",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="perspective_types.relationtype"),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CategoryPerspective",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "example",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="category", to="examples.example"
                    ),
                ),
                (
                    "perspective",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="perspective_types.categorytype"),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="BoundingBoxPerspective",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("x", models.FloatField()),
                ("y", models.FloatField()),
                ("width", models.FloatField()),
                ("height", models.FloatField()),
                (
                    "example",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="bbox", to="examples.example"
                    ),
                ),
                (
                    "perspective",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="perspective_types.categorytype"),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="TextPerspective",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("text", models.TextField()),
                (
                    "example",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="text_perspectives",
                        to="examples.example",
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "unique_together": {("example", "user", "text")},
            },
        ),
        migrations.AddConstraint(
            model_name="spanperspective",
            constraint=models.CheckConstraint(check=models.Q(("start_offset__gte", 0)), name="start_offset_gte_0"),
        ),
        migrations.AddConstraint(
            model_name="spanperspective",
            constraint=models.CheckConstraint(check=models.Q(("end_offset__gte", 0)), name="end_offset_gte_0"),
        ),
        migrations.AddConstraint(
            model_name="spanperspective",
            constraint=models.CheckConstraint(
                check=models.Q(("start_offset__lt", models.F("end_offset"))), name="start_lt_end"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="categoryperspective",
            unique_together={("example", "user", "perspective")},
        ),
        migrations.AddConstraint(
            model_name="boundingboxperspective",
            constraint=models.CheckConstraint(check=models.Q(("x__gte", 0)), name="x_gte_0"),
        ),
        migrations.AddConstraint(
            model_name="boundingboxperspective",
            constraint=models.CheckConstraint(check=models.Q(("y__gte", 0)), name="y_gte_0"),
        ),
        migrations.AddConstraint(
            model_name="boundingboxperspective",
            constraint=models.CheckConstraint(check=models.Q(("width__gte", 0)), name="width_gte_0"),
        ),
        migrations.AddConstraint(
            model_name="boundingboxperspective",
            constraint=models.CheckConstraint(check=models.Q(("height__gte", 0)), name="height_gte_0"),
        ),
    ]
