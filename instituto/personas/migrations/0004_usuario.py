# Generated by Django 5.1 on 2024-12-05 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0003_hora_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('grupo', models.CharField(choices=[('Paciente', 'Paciente'), ('Medico', 'Medico')], max_length=20)),
            ],
        ),
    ]
