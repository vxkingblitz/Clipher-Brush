# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paintings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='painting',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
