# Generated by Django 3.2.5 on 2023-11-01 15:13

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
            name='InterviewQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='InterviewRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.interviewquestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InterviewScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professional_score', models.PositiveIntegerField()),
                ('professional_suggestion', models.TextField()),
                ('creative_score', models.PositiveIntegerField()),
                ('creative_suggestion', models.TextField()),
                ('strategy_score', models.PositiveIntegerField()),
                ('strategy_suggestion', models.TextField()),
                ('communication_score', models.PositiveIntegerField()),
                ('communication_suggestion', models.TextField()),
                ('self_learning_score', models.PositiveIntegerField()),
                ('self_learning_suggestion', models.TextField()),
                ('comprehensive_score', models.PositiveIntegerField()),
                ('comprehensive_suggestion', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('records', models.ManyToManyField(to='contents.InterviewRecord')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DashBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContentRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('CL', '求職信'), ('RL', '推薦信'), ('R', '履歷'), ('SI', '自我介紹')], max_length=10)),
                ('unit', models.CharField(max_length=100)),
                ('result', models.TextField()),
                ('is_satisfied', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
