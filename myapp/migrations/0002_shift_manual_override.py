from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='manual_override',
            field=models.BooleanField(default=False),
        ),
    ] 