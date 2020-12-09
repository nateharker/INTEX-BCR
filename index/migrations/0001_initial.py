# Generated by Django 3.1.4 on 2020-12-07 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Joblisting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=5000)),
                ('city', models.CharField(max_length=50)),
                ('contracts', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='JobOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('contracts', models.CharField(max_length=2)),
                ('matching_skills', models.SmallIntegerField()),
                ('status', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=2)),
                ('sector', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='JobOfferSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proficiency', models.SmallIntegerField()),
                ('joboffer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.joboffer')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.skill')),
            ],
        ),
        migrations.AddField(
            model_name='joboffer',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.organization'),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='skills',
            field=models.ManyToManyField(through='index.JobOfferSkill', to='index.Skill'),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.user'),
        ),
        migrations.CreateModel(
            name='JobListingSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importance', models.SmallIntegerField()),
                ('job_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.joblisting')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.skill')),
            ],
        ),
        migrations.AddField(
            model_name='joblisting',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.organization'),
        ),
        migrations.AddField(
            model_name='joblisting',
            name='skills',
            field=models.ManyToManyField(through='index.JobListingSkill', to='index.Skill'),
        ),
    ]