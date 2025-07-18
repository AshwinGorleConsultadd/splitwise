# Generated by Django 4.2.22 on 2025-07-15 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='groups.group')),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owned_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='expenses.expense')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_shares', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('from_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depts_given', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='depts', to='groups.group')),
                ('to_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depts_received', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('from_member', 'to_member', 'group')},
            },
        ),
    ]
