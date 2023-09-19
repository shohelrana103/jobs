from __future__ import print_function
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
from rest_framework.decorators import api_view, permission_classes
from worker.models.worker import Worker
from common.models.gender import Gender
from common.models.country import Country
from common.models.state import State
from common.models.city import City
from common.models.area import Area
from common.models.degree import Degree
from worker.models.education import EducationHistory
from worker.models.skill import Skill
from django.conf import settings
from django.core.mail import send_mail
import os
from twilio.rest import Client

import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException
from common.views.zip_code import get_address_details


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
            try:
                worker_instance = Worker.objects.get(pk=auth_user.user_id, account_status=1)
            except:
                content['message'] = 'Account is not Valid'
                return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
        except Authentication.DoesNotExist:
            # creating user
            user_instance, is_create = User.objects.get_or_create(username=phone_number)
            # creating token
            token, create = Token.objects.get_or_create(user=user_instance)
            auth_user = Authentication.objects.create(user_phone=phone_number, username=phone_number, token=token.key,
                                                      user_type=2)
            # create worker
            worker, cr = Worker.objects.get_or_create(phone_number=phone_number)
            if cr:
                auth_user.user_id = worker.id
                auth_user.save()
        # write send otp code here
        otp = random.randint(100000, 999999)
        UserOtp.objects.create(auth_user=auth_user,
                               otp=otp,
                               otp_send_time=datetime.now())
        # # write otp send code here
        # Twilio code
        # account_sid = settings.TWILIO_ACCOUNT_SID
        # auth_token = settings.TWILIO_AUTH_TOKEN
        # client = Client(account_sid, auth_token)
        # message_body = 'Your OTP is ' + str(otp)
        # try:
        #     # for testing
        #     if phone_number == '+12345678910':
        #         content['status'] = 1
        #         content['message'] = 'OTP send successful'
        #         return JsonResponse(content, status=status.HTTP_200_OK)
        #     message = client.messages.create(
        #         body=message_body,
        #         from_='+14708023425',
        #         to=phone_number
        #     )
        # Configure HTTP basic authorization: BasicAuth
        configuration = clicksend_client.Configuration()
        configuration.username = settings.CLICKSEND_USERNAME
        configuration.password = settings.CLICKSEND_APIKEY

        # create an instance of the API class
        api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

        # If you want to explictly set from, add the key _from to the message.
        device_hash = ''
        if 'device_hash' in request.data:
            device_hash = request.data['device_hash']
        message_body = 'Your OTP is: ' + str(otp) + "\n" + device_hash
        sms_message = SmsMessage(source="php",
                                 body=message_body,
                                 to=phone_number)

        sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])

        try:
            # Send sms message(s)
            api_response = api_instance.sms_send_post(sms_messages)
            # print(api_response)
        except ApiException as e:
            print("Exception when calling SMSApi->sms_send_post: %s\n" % e)
        except Exception as e:
            content['message'] = 'Something wrong'
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
        # for testing purpose
        if phone_number == '+12345678910' or phone_number == '+8801752746973':
            user_otp.otp = 123456
        if user_otp and user_otp.otp == otp:
            auth_serialized = AuthenticationSerializer(auth_user)
            # worker details
            worker = Worker.objects.get(pk=auth_user.user_id)
            if worker.first_name and worker.address_line1 and worker.educations.all() and worker.skill_set.all():
                update_info = {"is_profile_update": True, "first_name": worker.first_name}
            else:
                update_info = {"is_profile_update": False, "first_name": None}
            update_info.update(auth_serialized.data)
            content['status'] = 1
            content['message'] = 'Success'
            content['data'] = update_info
            return JsonResponse(content, status=status.HTTP_200_OK)
        else:
            content['message'] = 'OTP Does Not Match!'
            return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def worker_send_otp_email(request):
    content = {
        'status': 0
    }
    if 'email' in request.data:
        email = request.data['email']
        # for testing
        if email == 'worker@workersrus.com':
            content['status'] = 1
            content['message'] = 'OTP send successful'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            auth_user = Authentication.objects.get(email=email)
            try:
                worker_instance = Worker.objects.get(pk=auth_user.user_id, account_status=1)
            except:
                content['message'] = 'Account is not Valid'
                return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
        except Authentication.DoesNotExist:
            # creating user
            user_instance = User.objects.create_user(email)
            # creating token
            token, create = Token.objects.get_or_create(user=user_instance)
            auth_user = Authentication.objects.create(email=email, username=email, token=token.key, user_type=2)
            # create worker
            worker, cr = Worker.objects.get_or_create(email=email)
            if cr:
                auth_user.user_id = worker.id
                auth_user.save()
        # write send otp code here
        otp = random.randint(100000, 999999)
        UserOtp.objects.create(auth_user=auth_user,
                               otp=otp,
                               otp_send_time=datetime.now())
        # send otp in email
        subject = 'OTP'
        message = 'Your OTP is ' + str(otp)
        email_from = settings.DEFAULT_FROM_EMAIL
        try:
            send_mail(
                subject,
                message,
                email_from,
                [email],
                fail_silently=False,
            )

        except Exception as e:
            pass
        content['status'] = 1
        content['message'] = 'OTP send successful'

    else:
        content['message'] = 'Require Parameter Missing'
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def worker_verify_otp_email(request):
    content = {
        'status': 0
    }
    if 'email' in request.data and 'otp' in request.data:
        email = request.data['email']
        otp = request.data['otp']
        try:
            auth_user = Authentication.objects.get(email=email)
        except Authentication.DoesNotExist:
            content['message'] = 'Something Wrong!'
            return JsonResponse(content, status=status.HTTP_200_OK)
        # write send otp code here
        user_otp = UserOtp.objects.filter(auth_user=auth_user).order_by('otp_send_time').last()
        # for testing purpose
        if email == 'worker@workersrus.com' or email == 'oahidzihad1@gmail.com':
            user_otp.otp = 123456
        if user_otp and user_otp.otp == int(otp):
            auth_serialized = AuthenticationSerializer(auth_user)
            # worker details
            worker = Worker.objects.get(pk=auth_user.user_id)
            if worker.first_name and worker.country and worker.address_line1 and worker.educations.all() and worker.skill_set.all():
                update_info = {"is_profile_update": True, "first_name": worker.first_name}
            else:
                update_info = {"is_profile_update": False, "first_name": None}
            update_info.update(auth_serialized.data)
            content['status'] = 1
            content['message'] = 'Success'
            content['data'] = update_info
            return JsonResponse(content, status=status.HTTP_200_OK)
        else:
            content['message'] = 'OTP Does Not Match!'
            return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def worker_set_basic_information(request):
    content = {
        'status': 0
    }
    error_message = {}
    if 'user_id' in request.data:
        user_id = request.data['user_id']
    else:
        error_message['userId'] = ["This field is required"]
    if 'first_name' in request.data:
        first_name = request.data['first_name']
    else:
        error_message['firstName'] = ["This field is required"]
    if 'date_of_birth' in request.data:
        date_of_birth = request.data['date_of_birth']
    else:
        error_message['dateOfBirth'] = ["This field is required"]
    if 'gender_id' in request.data:
        gender_id = request.data['gender_id']
    else:
        error_message['genderId'] = ["This field is required"]
    if len(error_message) != 0:
        content['message'] = 'Invalid data'
        content['error'] = error_message
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
    try:
        worker = Worker.objects.get(pk=user_id)
    except Worker.DoesNotExist:
        content['message'] = 'Worker Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    try:
        gender = Gender.objects.get(pk=gender_id)
    except:
        gender = None
    worker.first_name = first_name
    worker.date_of_birth = date_of_birth
    worker.gender = gender
    if 'middle_name' in request.data:
        worker.middle_name = request.data['middle_name']
    if 'last_name' in request.data:
        worker.last_name = request.data['last_name']
    if 'email' in request.data:
        worker.email = request.data['email']
    if 'linkedin_profile' in request.data:
        worker.linkedin_profile = request.data['linkedin_profile']
    if 'phone_number' in request.data:
        worker.phone_number = request.data['phone_number']
    if 'passport_number' in request.data:
        worker.passport_number = request.data['passport_number']
    worker.save()
    content['status'] = 1
    content['message'] = 'Success'
    return JsonResponse(content, status=status.HTTP_200_OK)
    # if all(k in request.data for k in ("user_id", "first_name", "date_of_birth", "gender_id")):
    #     user_id = request.data['user_id']
    #     first_name = request.data['first_name']
    #     date_of_birth = request.data['date_of_birth']
    #     gender_id = request.data['gender_id']
    #     try:
    #         worker = Worker.objects.get(pk=user_id)
    #     except Worker.DoesNotExist:
    #         content['message'] = 'Worker Not Found'
    #         return JsonResponse(content, status=status.HTTP_200_OK)
    #     try:
    #         gender = Gender.objects.get(pk=gender_id)
    #     except:
    #         gender = None
    #     worker.first_name = first_name
    #     worker.date_of_birth = date_of_birth
    #     worker.gender = gender
    #     if 'middle_name' in request.data:
    #         worker.middle_name = request.data['middle_name']
    #     if 'last_name' in request.data:
    #         worker.last_name = request.data['last_name']
    #     if 'email' in request.data:
    #         worker.email = request.data['email']
    #     worker.save()
    #     content['status'] = 1
    #     content['message'] = 'Success'
    #     return JsonResponse(content, status=status.HTTP_200_OK)
    # else:
    #     content['message'] = 'Parameter Missing!'
    #     return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def worker_set_address(request):
    content = {
        'status': 0
    }
    error_message = {}
    if 'user_id' in request.data:
        user_id = request.data['user_id']
    else:
        error_message['userId'] = ["This field is required"]
    # if 'country_id' in request.data:
    #     country_id = request.data['country_id']
    # else:
    #     error_message['countryId'] = ["This field is required"]
    # if 'state_id' in request.data:
    #     state_id = request.data['state_id']
    # else:
    #     error_message['stateId'] = ["This field is required"]
    # if 'city_id' in request.data:
    #     city_id = request.data['city_id']
    # else:
    #     error_message['cityId'] = ["This field is required"]
    # if 'area_id' in request.data:
    #     area_id = request.data['area_id']
    # else:
    #     error_message['areaId'] = ["This field is required"]
    if 'address_line1' in request.data:
        address_line1 = request.data['address_line1']
    else:
        error_message['addressLine1'] = ["This field is required"]
    if 'zip_code' in request.data:
        zip_code = request.data['zip_code']
    else:
        error_message['zipCode'] = ["This field is required"]
    if len(error_message) != 0:
        content['message'] = 'Invalid data'
        content['error'] = error_message
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
    try:
        worker = Worker.objects.get(pk=user_id)
    except Worker.DoesNotExist:
        content['message'] = 'Worker Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    # try:
    #     country = Country.objects.get(pk=country_id)
    # except:
    #     content['message'] = 'Country Not Found'
    #     return JsonResponse(content, status=status.HTTP_200_OK)
    # try:
    #     state = State.objects.get(pk=state_id)
    # except:
    #     content['message'] = 'State Not Found'
    #     return JsonResponse(content, status=status.HTTP_200_OK)
    # try:
    #     city = City.objects.get(pk=city_id)
    # except:
    #     content['message'] = 'City Not Found'
    #     return JsonResponse(content, status=status.HTTP_200_OK)
    # try:
    #     area = Area.objects.get(pk=area_id)
    # except:
    #     content['message'] = 'Area Not Found'
    #     return JsonResponse(content, status=status.HTTP_200_OK)
    # country, city, state = get_address_details(zip_code)
    # worker.country = country
    # worker.state = state
    # worker.city = city
    # worker.area = area
    worker.address_line1 = address_line1
    worker.zip_code = zip_code
    worker.zip_address = get_address_details(zip_code)
    if 'address_line2' in request.data:
        worker.address_line2 = request.data['address_line2']
    worker.save()
    content['status'] = 1
    content['message'] = 'Success'
    return JsonResponse(content, status=status.HTTP_200_OK)
    # if all(k in request.data for k in
    #        ("user_id", "country_id", "state_id", "city_id", "area_id", "address_line1", "postal_code")):
    #     user_id = request.data['user_id']
    #     country_id = request.data['country_id']
    #     state_id = request.data['state_id']
    #     city_id = request.data['city_id']
    #     area_id = request.data['area_id']
    #     address_line1 = request.data['address_line1']
    #     postal_code = request.data['postal_code']
    #     try:
    #         worker = Worker.objects.get(pk=user_id)
    #     except Worker.DoesNotExist:
    #         content['message'] = 'Worker Not Found'
    #         return JsonResponse(content, status=status.HTTP_200_OK)
    #     try:
    #         country = Country.objects.get(pk=country_id)
    #     except:
    #         content['message'] = 'Country Not Found'
    #         return JsonResponse(content, status=status.HTTP_200_OK)
    #     try:
    #         state = State.objects.get(pk=state_id)
    #     except:
    #         content['message'] = 'State Not Found'
    #         return JsonResponse(content, status=status.HTTP_200_OK)
    #     try:
    #         city = City.objects.get(pk=city_id)
    #     except:
    #         content['message'] = 'City Not Found'
    #         return JsonResponse(content, status=status.HTTP_200_OK)
    #     try:
    #         area = Area.objects.get(pk=area_id)
    #     except:
    #         content['message'] = 'Area Not Found'
    #         return JsonResponse(content, status=status.HTTP_200_OK)
    #     worker.country = country
    #     worker.state = state
    #     worker.city = city
    #     worker.area = area
    #     worker.address_line1 = address_line1
    #     worker.postal_code = postal_code
    #     if 'address_line2' in request.data:
    #         worker.address_line2 = request.data['address_line2']
    #     worker.save()
    #     content['status'] = 1
    #     content['message'] = 'Success'
    #     return JsonResponse(content, status=status.HTTP_200_OK)
    # else:
    #     content['message'] = 'Parameter Missing!'
    #     return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def worker_set_education(request):
    content = {
        'status': 0
    }
    error_message = {}
    if 'user_id' in request.data:
        user_id = request.data['user_id']
    else:
        error_message['userId'] = ["This field is required"]
    if 'degree_list' in request.data:
        degree_list = request.data['degree_list']
    else:
        error_message['degreeList'] = ["This field is required"]
    if len(error_message) != 0:
        content['message'] = 'Invalid data'
        content['error'] = error_message
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
    try:
        worker = Worker.objects.get(pk=user_id)
    except Worker.DoesNotExist:
        content['message'] = 'Worker Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    education_list = []
    for degree in degree_list:
        try:
            degree_obj = Degree.objects.get(pk=degree['degree_id'])
        except:
            content['message'] = 'Degree Not Found'
            return JsonResponse(content, status=status.HTTP_404_NOT_FOUND)
        if degree['passing_year']:
            passing_year = degree['passing_year']
        else:
            passing_year = None
        if degree['result']:
            result = degree['result']
        else:
            result = None
        try:
            education_obj = worker.educations.get(degree=degree_obj)
            # education_obj = EducationHistory.objects.get(degree=degree_obj)
            education_obj.institute = degree['institute']
            education_obj.passing_year = passing_year
            education_obj.is_currently_reading = bool(degree['is_currently_reading'])
            education_obj.result = result
            education_obj.save()
        except Exception as e:
            education_obj = EducationHistory.objects.create(degree=degree_obj, institute=degree['institute'],
                                                            passing_year=passing_year,
                                                            is_currently_reading=bool(
                                                                degree['is_currently_reading']),
                                                            result=result)
            education_list.append(education_obj)
            # worker.educations.clear()
    worker.educations.add(*education_list)
    worker.save()
    content['status'] = 1
    content['message'] = 'Success'
    return JsonResponse(content, status=status.HTTP_200_OK)
    # if all(k in request.data for k in ("user_id", "degree_list")):
    #     user_id = request.data['user_id']
    #     degree_list = request.data['degree_list']
    #     try:
    #         worker = Worker.objects.get(pk=user_id)
    #     except Worker.DoesNotExist:
    #         content['message'] = 'Worker Not Found'
    #         return JsonResponse(content, status=status.HTTP_200_OK)
    #     education_list = []
    #     for degree in degree_list:
    #         try:
    #             degree_obj = Degree.objects.get(pk=degree['degree_id'])
    #         except:
    #             content['message'] = 'Degree Not Found'
    #             return JsonResponse(content, status=status.HTTP_200_OK)
    #         if degree['passing_year']:
    #             passing_year = degree['passing_year']
    #         else:
    #             passing_year = None
    #         if degree['result']:
    #             result = degree['result']
    #         else:
    #             result = None
    #         try:
    #             education_obj = worker.educations.get(degree=degree_obj)
    #             # education_obj = EducationHistory.objects.get(degree=degree_obj)
    #             education_obj.institute = degree['institute']
    #             education_obj.passing_year = passing_year
    #             education_obj.is_currently_reading = bool(degree['is_currently_reading'])
    #             education_obj.result = result
    #             education_obj.save()
    #             print(education_obj.result)
    #         except Exception as e:
    #             education_obj = EducationHistory.objects.create(degree=degree_obj, institute=degree['institute'],
    #                                                             passing_year=passing_year,
    #                                                             is_currently_reading=bool(
    #                                                                 degree['is_currently_reading']),
    #                                                             result=result)
    #             education_list.append(education_obj)
    #     worker.educations.add(*education_list)
    #     worker.save()
    #     content['status'] = 1
    #     content['message'] = 'Success'
    #     return JsonResponse(content, status=status.HTTP_200_OK)
    # else:
    #     content['message'] = 'Parameter Missing!'
    #     return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def worker_set_skill(request):
    content = {
        'status': 0
    }
    error_message = {}
    if 'user_id' in request.data:
        user_id = request.data['user_id']
    else:
        error_message['userId'] = ["This field is required"]
    if 'skill_list' in request.data:
        skill_list = request.data['skill_list']
    else:
        error_message['skillList'] = ["This field is required"]
    if len(error_message) != 0:
        content['message'] = 'Invalid data'
        content['error'] = error_message
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
    try:
        worker = Worker.objects.get(pk=user_id)
    except Worker.DoesNotExist:
        content['message'] = 'Worker Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    skills = []
    for skill in skill_list:
        skill_obj, create = Skill.objects.get_or_create(skill_name=skill)
        skills.append(skill_obj)
    worker.skill_set.add(*skills)
    worker.save()
    content['status'] = 1
    content['message'] = 'Success'
    return JsonResponse(content, status=status.HTTP_200_OK)
    # if all(k in request.data for k in ("user_id", "skill_list")):
    #     user_id = request.data['user_id']
    #     skill_list = request.data['skill_list']
    #     try:
    #         worker = Worker.objects.get(pk=user_id)
    #     except Worker.DoesNotExist:
    #         content['message'] = 'Worker Not Found'
    #         return JsonResponse(content, status=status.HTTP_200_OK)
    #     skills = []
    #     for skill in skill_list:
    #         skill_obj, create = Skill.objects.get_or_create(skill_name=skill)
    #         skills.append(skill_obj)
    #     worker.skill_set.add(*skills)
    #     worker.save()
    #     content['status'] = 1
    #     content['message'] = 'Success'
    #     return JsonResponse(content, status=status.HTTP_200_OK)
    # else:
    #     content['message'] = 'Parameter Missing!'
    #     return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def worker_signup(request):
    content = {
        'status': 0
    }
    if 'first_name' in request.data and 'last_name' in request.data and 'phone_number' in request.data:
        phone_number = request.data['phone_number']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        auth_user = Authentication.objects.filter(user_phone=phone_number).first()
        if auth_user:
            content['message'] = "This phone number already used"
            return JsonResponse(content, status=status.HTTP_200_OK)
        else:
            # creating user
            user_instance = User.objects.create_user(phone_number)
            # user_instance, is_create = User.objects.get_or_create()
            # creating token
            token, create = Token.objects.get_or_create(user=user_instance)
            auth_user = Authentication.objects.create(user_phone=phone_number, username=phone_number, token=token.key,
                                                      user_type=2)
            # create worker
            worker, cr = Worker.objects.get_or_create(phone_number=phone_number)
            if cr:
                worker.first_name = first_name
                worker.last_name = last_name
                worker.save()
                auth_user.user_id = worker.id
                auth_user.save()
            if worker.first_name and worker.address_line1 and worker.educations.all() and worker.skill_set.all():
                update_info = {"is_profile_update": True, "first_name": worker.first_name}
            else:
                update_info = {"is_profile_update": False, "first_name": worker.first_name}
            auth_serialized = AuthenticationSerializer(auth_user)
            update_info.update(auth_serialized.data)
        content['status'] = 1
        content['message'] = 'Signup successful'
        content['data'] = update_info

    else:
        content['message'] = 'Require Parameter Missing'
    return JsonResponse(content, status=status.HTTP_200_OK)
