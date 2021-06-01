from rest_framework import serializers

from .models import *


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['value']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['value']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['value']


class ApplicantShowSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    likes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='value')
    matches = serializers.SlugRelatedField(many=True, read_only=True, slug_field='value')

    class Meta:
        model = Applicant
        fields = ['id', 'name', 'surname', 'age', 'region', 'email', 'skills', 'relocate', 'desc',
                  'likes', 'dislike', 'matches']


class ApplicantSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Applicant
        fields = ['id', 'name', 'surname', 'age', 'region', 'email', 'skills', 'relocate', 'desc',
                  'likes', 'dislike', 'matches']

    def create(self, validated_data):
        skills = validated_data.pop('skills')

        applicant = Applicant.objects.create(**validated_data)
        for skill in skills:
            applicant.skills.create(**skill)

        return applicant


class CompanyShowSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    likes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='value')
    matches = serializers.SlugRelatedField(many=True, read_only=True, slug_field='value')

    class Meta:
        model = Company
        fields = ['id', 'name', 'age', 'region', 'skills', 'desc', 'likes', 'dislike', 'matches']


class CompanySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'age', 'region', 'skills', 'desc', 'likes', 'matches']

    def create(self, validated_data):
        skills = validated_data.pop('skills')

        company = Company.objects.create(**validated_data)
        for skill in skills:
            company.skills.create(**skill)

        return company
