# Generated manually to support MPTT conversion on existing Category rows

import django.db.models.deletion
from django.db import migrations, models


def seed_category_tree_fields(apps, schema_editor):
    Category = apps.get_model('learningApp', 'Category')
    for index, category in enumerate(Category.objects.order_by('id'), start=1):
        category.level = 0
        category.lft = 1
        category.rght = 2
        category.tree_id = index
        category.save(update_fields=['level', 'lft', 'rght', 'tree_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('learningApp', '0003_courseanalytics_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='children',
                to='learningApp.category',
            ),
        ),
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.RunPython(seed_category_tree_fields, migrations.RunPython.noop),
    ]