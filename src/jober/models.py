from django.db import models


class Like(models.Model):
    value = models.IntegerField()


class Match(models.Model):
    value = models.IntegerField()


class Skill(models.Model):
    skill = [
        ('1', 'Python'),
        ('2', 'Django'),
        ('3', 'DRF'),
        ('4', 'JavaScript'),
        ('5', 'VUE.js'),
        ('6', 'React'),
        ('7', 'C#'),
        ('8', 'ASP.NET')
    ]
    value = models.CharField(choices=skill, max_length=3, default='1')


class Applicant(models.Model):
    name = models.CharField(max_length=25, blank=False)
    surname = models.CharField(max_length=25, blank=False)
    age = models.IntegerField(blank=False)
    region = models.IntegerField(blank=False)
    email = models.EmailField(blank=True)
    skills = models.ManyToManyField(Skill, blank=False)
    relocate = models.BooleanField(default=False)
    desc = models.TextField()
    likes = models.ManyToManyField(Like, related_name='likes', blank=True)
    matches = models.ManyToManyField(Match, related_name='matches', blank=True)

    def __str__(self):
        return f"User: {self.name}"


class Company(models.Model):
    name = models.CharField(max_length=25)
    age = models.IntegerField(blank=False)
    region = models.IntegerField(blank=False)
    skills = models.ManyToManyField(Skill, blank=False)
    desc = models.TextField()
    likes = models.ManyToManyField(Like, related_name='likes_company', blank=True)
    matches = models.ManyToManyField(Match, related_name='matches_company', blank=True)

    def __str__(self):
        return f"name: {self.name}"
