from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Sport, Registration, Team
from .serializers import SportSerializer, RegistrationSerializer, TeamSerializer

# Sport Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sport_list(request):
    if request.method == 'GET':
        sports = Sport.objects.all()
        serializer = SportSerializer(sports, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = SportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(primary=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def sport_detail(request, pk):
    sport = get_object_or_404(Sport, pk=pk)
    
    if request.method == 'GET':
        serializer = SportSerializer(sport)
        return Response(serializer.data)
    
    # Only primary or secondary coordinators can modify
    if request.user != sport.primary and request.user not in sport.secondary.all():
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = SportSerializer(sport, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        sport.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Registration Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def registration_list(request):
    if request.method == 'GET':
        # If user is a coordinator, show all registrations for their sports
        coordinated_sports = Sport.objects.filter(
            Q(primary=request.user) | Q(secondary=request.user)
        )
        if coordinated_sports.exists():
            registrations = Registration.objects.filter(sport__in=coordinated_sports)
        else:
            # Otherwise show only user's registrations
            registrations = Registration.objects.filter(student=request.user)
        
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def registration_detail(request, pk):
    registration = get_object_or_404(Registration, pk=pk)
    
    # Check if user is authorized
    if (request.user != registration.student and 
        request.user != registration.sport.primary and 
        request.user not in registration.sport.secondary.all()):
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = RegistrationSerializer(registration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Team Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def team_list(request):
    if request.method == 'GET':
        # If user is a coordinator, show all teams for their sports
        coordinated_sports = Sport.objects.filter(
            Q(primary=request.user) | Q(secondary=request.user)
        )
        if coordinated_sports.exists():
            teams = Team.objects.filter(sport__in=coordinated_sports)
        else:
            # Otherwise show teams user is a member of
            teams = Team.objects.filter(members=request.user)
        
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure the sport exists and is a team sport
            sport = get_object_or_404(Sport, pk=serializer.validated_data['sport_id'])
            if not sport.isTeamBased:
                return Response(
                    {"error": "This sport does not support teams"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    
    # Check if user is authorized (coordinator or team member)
    if (request.user not in team.members.all() and 
        request.user != team.sport.primary and 
        request.user not in team.sport.secondary.all()):
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = TeamSerializer(team)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Only coordinators can delete teams
        if (request.user != team.sport.primary and 
            request.user not in team.sport.secondary.all()):
            return Response(status=status.HTTP_403_FORBIDDEN)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
