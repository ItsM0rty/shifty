from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_shift_manual_override'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ] 