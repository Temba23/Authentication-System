# Generated by Django 5.0.3 on 2024-06-13 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_securityquestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='securityquestion',
            name='questions',
            field=models.CharField(choices=[(1, 'What is mothers name ?'), (2, 'What was the name of your first pet ?'), (3, 'What school you graduated from ?'), (4, 'What is your favorite color ?'), (5, 'How many siblings you have ?')], max_length=60),
        ),
    ]
