# Generated by Django 4.2.2 on 2023-06-20 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeapp', '0008_alter_assignmentmarks_marks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='Password',
            field=models.CharField(default='admin', max_length=255),
        ),
        migrations.AlterField(
            model_name='faculties',
            name='Pass',
            field=models.CharField(default='null', max_length=255),
        ),
        migrations.AlterField(
            model_name='students',
            name='Pass',
            field=models.CharField(default='null', max_length=255),
        ),
    ]