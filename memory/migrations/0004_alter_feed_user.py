# Generated by Django 4.2.14 on 2024-08-04 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0003_alter_personalcomment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memory.user'),
        ),
    ]
