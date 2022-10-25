# Generated by Django 4.1.2 on 2022-10-25 10:11

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modification Date and Time')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(max_length=200, verbose_name='Slug')),
                ('content', models.TextField(verbose_name='Content')),
                ('publishing_status', models.CharField(choices=[('d', 'Draft'), ('p', 'Published')], default='d', max_length=1, verbose_name='Publishing status')),
                ('image', models.ImageField(upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
            managers=[
                ('custom_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
