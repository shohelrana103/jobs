from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.authentication import Authentication, AuthenticationSerializer
from ..models.user_otp import UserOtp
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import random
from datetime import datetime


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def worker_send_otp(request):
    content = {
        'status': 0
    }
    if 'phone_number' in request.data:
        phone_number = request.data['phone_number']
        try:
            auth_user = Authentication.objects.get(user_phone=phone_number)
        except Authentication.DoesNotExist:
            # creating user
            user_instance, is_create = User.objects.get_or_create(phone_number)
            # creating token
            token, create = Token.objects.get_or_create(user=user_instance)
            auth_user = Authentication.objects.create(user_phone=phone_number, token=token.key, user_type=2)
        # write send otp code here
        otp = random.randint(100000, 999999)
        UserOtp.objects.create(auth_user=auth_user,
                               otp=otp,
                               otp_send_time=datetime.now())
        # write otp send code here
        content['status'] = 1
        content['message'] = 'OTP send successful'

    else:
        content['message'] = 'Require Parameter Missing'
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def worker_verify_otp(request):
    content = {
        'status': 0
    }
    if 'phone_number' in request.data and 'otp' in request.data:
        phone_number = request.data['phone_number']
        otp = request.data['otp']
        try:
            auth_user = Authentication.objects.get(user_phone=phone_number)
        except Authentication.DoesNotExist:
            content['message'] = 'Something Wrong!'
            return JsonResponse(content, status=status.HTTP_200_OK)
        # write send otp code here
        user_otp = UserOtp.objects.filter(auth_user=auth_user).order_by('otp_send_time').last()
        if user_otp and user_otp.otp == otp:
            auth_serialized = AuthenticationSerializer(auth_user)
            content['status'] = 1
            content['message'] = 'Success'
            content['data'] = auth_serialized.data
            return JsonResponse(content, status=status.HTTP_200_OK)
        else:
            content['message'] = 'OTP Does Not Match!'
            return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)
