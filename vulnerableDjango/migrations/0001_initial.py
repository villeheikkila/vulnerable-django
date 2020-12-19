from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                               related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('message', models.TextField()),
            ],
        ),
    ]
