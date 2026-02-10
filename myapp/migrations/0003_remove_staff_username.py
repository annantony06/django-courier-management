from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_staff_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='username',
        ),
    ]
