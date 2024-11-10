import datetime
import os
from time import timezone
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated 
from django.utils.crypto import get_random_string
from .models import Profile
from django.core.mail import send_mail

# Create your views here.

@api_view(['POST'])
def register(request):
    registration_data = request.data
    user_serializer = RegisterSerializer(data=registration_data)

    if user_serializer.is_valid():
        if not User.objects.filter(email=registration_data['email']).exists():
            user_serializer = User.objects.create(
                first_name=registration_data['first_name'],
                last_name=registration_data['last_name'],
                email=registration_data['email'],
                username=registration_data['email'],
                password=make_password(registration_data['password']))
            return Response({'details': 'User created successfully'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Email already exists!'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user_serializer = UserSerializer(request.user, many=False)
    return Response(user_serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    user_data = request.data

    user.first_name = user_data['first_name']
    user.last_name = user_data['last_name']
    user.email = user_data['email']
    if user_data['password'] != '':
        user.password = make_password(user_data['password'])
    user.save()
    user_serializer = UserSerializer(user, many=False)

    return Response(user_serializer.data, status=status.HTTP_200_OK)

def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return f'{protocol}://{host}'


from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone

@api_view(['POST'])
def forget_password(request):
    data = request.data
    try:
        user = get_object_or_404(User, email=data['email'])
        if hasattr(user, 'profile'): 
            user.profile.reset_password_token = get_random_string(40)
            user.profile.reset_password_expire = timezone.now() + timezone.timedelta(minutes=30)
            user.profile.save()
        else:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
            pass  
        email_content = f"Hello {user.first_name},\n\nPlease click the link below to reset your password:\n\n{get_current_host(request)}/api/reset_password/{user.profile.reset_password_token}\n\nThis link will expire in 30 minutes.\n\nThanks,\nFarmFlow Team"

        send_mail(
            subject="Password Reset for FarmFlow Account",
            message=email_content,
            from_email=os.getenv('EMAIL_HOST_USER'),  
            recipient_list=[data['email']],
            fail_silently=False,  
        )

        return Response({'details': 'Password reset sent to {email}'.format(email=data['email'])})
    except User.DoesNotExist:
        return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error sending password reset email: {e}")  
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
@api_view(['POST'])
def reset_password(request,token):
    data = request.data
    user = get_object_or_404(User,profile__reset_password_token=token)
    if user.profile.reset_password_expire < timezone.now():
        return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST) 
    
    if data['password'] == '':
        return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)


    if data['password'] == data['confirm_password']:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()
    return Response({'details': 'Password reset successfully'}, status=status.HTTP_200_OK)

                
    