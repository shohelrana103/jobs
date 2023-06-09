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
    if all(k in request.data for k in ("user_id", "first_name", "date_of_birth", "gender_id")):
        user_id = request.data['user_id']
        first_name = request.data['first_name']
        date_of_birth = request.data['date_of_birth']
        gender_id = request.data['gender_id']
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
        worker.save()
        content['status'] = 1
        content['message'] = 'Success'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def worker_set_address(request):
    content = {
        'status': 0
    }
    if all(k in request.data for k in ("user_id", "country_id", "state_id", "city_id", "area_id", "address_line1", "postal_code")):
        user_id = request.data['user_id']
        country_id = request.data['country_id']
        state_id = request.data['state_id']
        city_id = request.data['city_id']
        area_id = request.data['area_id']
        address_line1 = request.data['address_line1']
        postal_code = request.data['postal_code']
        try:
            worker = Worker.objects.get(pk=user_id)
        except Worker.DoesNotExist:
            content['message'] = 'Worker Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            country = Country.objects.get(pk=country_id)
        except:
            content['message'] = 'Country Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            state = State.objects.get(pk=state_id)
        except:
            content['message'] = 'State Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            city = City.objects.get(pk=city_id)
        except:
            content['message'] = 'City Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            area = Area.objects.get(pk=area_id)
        except:
            content['message'] = 'Area Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        worker.country = country
        worker.state = state
        worker.city = city
        worker.area = area
        worker.address_line1 = address_line1
        worker.postal_code = postal_code
        if 'address_line2' in request.data:
            worker.address_line2 = request.data['address_line2']
        worker.save()
        content['status'] = 1
        content['message'] = 'Success'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def worker_set_education(request):
    content = {
        'status': 0
    }
    if all(k in request.data for k in ("user_id", "degree_list")):
        user_id = request.data['user_id']
        degree_list = request.data['degree_list']
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
                return JsonResponse(content, status=status.HTTP_200_OK)
            if degree['passing_year']:
                passing_year = degree['passing_year']
            else:
                passing_year = None
            education_obj = EducationHistory.objects.create(degree=degree_obj, institute=degree['institute'],
                                                     passing_year=passing_year, is_currently_reading=bool(degree['is_currently_reading']))
            education_list.append(education_obj)
        worker.educations.add(*education_list)
        worker.save()
        content['status'] = 1
        content['message'] = 'Success'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def worker_set_skill(request):
    Worker.objects.all().delete()
    # content = {
    #     'status': 0
    # }
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
    return JsonResponse({"OK":"OK"}, status=status.HTTP_200_OK)