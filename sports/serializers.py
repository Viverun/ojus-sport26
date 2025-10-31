from rest_framework import serializers
from .models import Sport, Registration, Team
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class SportSerializer(serializers.ModelSerializer):
    primary = UserSerializer(read_only=True)
    secondary = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Sport
        fields = ['id', 'name', 'description', 'team', 'primary', 'secondary']

class RegistrationSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    sport = SportSerializer(read_only=True)
    sport_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Registration
        fields = ['id', 'student', 'sport', 'sport_id', 'year', 'branch', 
                 'registered_on', 'registration_modified']
        read_only_fields = ['registered_on', 'registration_modified']

class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    sport = SportSerializer(read_only=True)
    sport_id = serializers.IntegerField(write_only=True)
    member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'branch', 'sport', 'sport_id', 'members', 'member_ids']

    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        team = Team.objects.create(**validated_data)
        if member_ids:
            team.members.set(User.objects.filter(id__in=member_ids))
        return team

    def update(self, instance, validated_data):
        member_ids = validated_data.pop('member_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if member_ids is not None:
            instance.members.set(User.objects.filter(id__in=member_ids))
        return instance