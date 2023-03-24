# Generated by Django 4.0.6 on 2023-03-12 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0010_tutee_alter_appointment_tutee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to='videos/')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tutor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]