from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.authentication import Authentication, AuthenticationSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password, check_password
from company.models.company import Company


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def company_signup(request):
    content = {
        'status': 0
    }
    if 'company_name' in request.data and 'email' in request.data and 'phone_number' in request.data and 'password' in request.data:
        phone_number = request.data['phone_number']
        company_name = request.data['company_name']
        email = request.data['email']
        password = request.data['password']
        auth_user_phone = Authentication.objects.filter(user_phone=phone_number).first()
        if auth_user_phone:
            content['message'] = "This phone number already used"
            return JsonResponse(content, status=status.HTTP_200_OK)
        auth_user_email = Authentication.objects.filter(email=email).first()
        if auth_user_email:
            content['message'] = "This email already used"
            return JsonResponse(content, status=status.HTTP_200_OK)
        # creating user
        user_instance = User.objects.create_user(email, email, password)
        # user_instance, is_create = User.objects.get_or_create()
        # creating token
        token, create = Token.objects.get_or_create(user=user_instance)
        auth_user = Authentication.objects.create(user_phone=phone_number,
                                                  username=email,
                                                  email=email,
                                                  token=token.key,
                                                  password=make_password(password),
                                                  user_type=1)
        # create company
        company = Company.objects.create(company_name=company_name, company_email=email)
        auth_user.user_id = company.id
        auth_user.save()

        update_info = {"company_name": company_name}
        auth_serialized = AuthenticationSerializer(auth_user)
        update_info.update(auth_serialized.data)
        content['status'] = 1
        content['message'] = 'Signup successful'
        content['data'] = update_info
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Require Parameter Missing'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def company_login(request):
    content = {
        "status": 0
    }
    if 'email' in request.data and 'password' in request.data:
        email = request.data.get('email')
        password = request.data.get('password')
        auth_user = Authentication.objects.filter(email__iexact=email)
        if auth_user.count() == 1:
            auth_user = auth_user.first()
            if check_password(password, auth_user.password):
                company = Company.objects.get(pk=auth_user.user_id)
                update_info = {"company_name": company.company_name}
                auth_serialized = AuthenticationSerializer(auth_user)
                update_info.update(auth_serialized.data)
                content['status'] = 1
                content['message'] = 'Login successful'
                content['data'] = update_info
                return JsonResponse(content, status=status.HTTP_200_OK)
            else:
                content['message'] = "one or both fields invalid"
                return JsonResponse(content, status=status.HTTP_200_OK)
        elif auth_user.count() > 1:
            content['message'] = "Something wrong!"
            return JsonResponse(content, status=status.HTTP_200_OK)
        else:
            content['message'] = "one or both fields invalid"
            return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Require Parameter Missing'
        return JsonResponse(content, status=status.HTTP_200_OK)