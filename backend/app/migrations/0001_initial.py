import random
import faker
import django.db.models.deletion
from django.db import migrations, models


def gen_dummy_data(apps, schema_editor):
    Category = apps.get_model("app", "Category")
    Book = apps.get_model("app", "Book")

    fake = faker.Faker()
    tags = fake.words(random.randint(1, 30))
    categories = []
    for i in fake.words(10):
        categories.append(Category.objects.create(name=i))

    for _ in range(200):
        Book.objects.create(
            name=fake.sentence(5),
            category=categories[random.randint(0, len(categories) - 1)],
            tags=";".join(
                fake.words(
                    random.randint(1, 5),
                    ext_word_list=tags,
                )
            ),
        )


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=256)),
                ("description", models.TextField(default="")),
            ],
        ),
        migrations.CreateModel(
            name="Book",
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
                ("name", models.CharField(max_length=256)),
                ("author", models.CharField(max_length=256)),
                ("tags", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="app.category"
                    ),
                ),
            ],
        ),
    ]
