from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from ..models.company import Company, CompanySerializer, CompanyDetailsSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..models.industry import Industry
from common.models.country import Country
from common.models.state import State
from common.models.city import City
from common.models.area import Area
from worker.models.job_application import JobApplication
from job.models.job import Job, JobSerializer
from worker.models.worker import Worker, WorkerSerializer, WorkerDetailsSerializer
from datetime import datetime
from common.views.zip_code import get_address_details


class CompanyView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, company_id):
        try:
            company = Company.objects.get(pk=company_id)
        except:
            content = {
                'status': 0,
                'message': 'Company Not Found',
            }
            return JsonResponse(content, status=status.HTTP_200_OK)
        serialized_company = CompanyDetailsSerializer(company, context={'request': request})
        content = {
            'status': 1,
            'message': 'Success',
            'data': serialized_company.data
        }
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_all_company(request):
    content = {
        'status': 0
    }
    companies = Company.objects.all()
    serialized_jobs = CompanySerializer(companies, many=True, context={'request': request})
    content['status'] = 1
    content['message'] = 'Success'
    content['companies'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def company_profile_update(request):
    content = {
        'status': 0
    }
    error_message = {}
    if 'user_id' in request.data:
        user_id = request.data['user_id']
    else:
        error_message['userId'] = ["This field is required"]
    if 'industry_id' in request.data:
        industry_id = request.data['industry_id']
    else:
        error_message['industryId'] = ["This field is required"]

    if 'address' in request.data:
        address = request.data['address']
    else:
        error_message['address'] = ["This field is required"]

    if 'company_name' in request.data:
        company_name = request.data['company_name']
    else:
        error_message['companyName'] = ["This field is required"]
    if 'company_email' in request.data:
        company_email = request.data['company_email']
    else:
        error_message['CompanyEmail'] = ["This field is required"]
    if 'phone_number' in request.data:
        phone_number = request.data['phone_number']
    else:
        error_message['phoneNumber'] = ["This field is required"]
    if 'about_company' in request.data:
        about_company = request.data['about_company']
    else:
        error_message['aboutCompany'] = ["This field is required"]
    if 'company_size' in request.data:
        company_size = request.data['company_size']
    else:
        error_message['companySize'] = ["This field is required"]
    if 'zip_code' in request.data:
        zip_code = request.data['zip_code']
    else:
        error_message['zipCode'] = ["This field is required"]
    if 'contact_person_name' in request.data:
        contact_person_name = request.data['contact_person_name']
    else:
        error_message['contactPersonName'] = ["This field is required"]
    if 'contact_person_position' in request.data:
        contact_person_position = request.data['contact_person_position']
    else:
        error_message['contactPersonPosition'] = ["This field is required"]
    if 'contact_person_mobile' in request.data:
        contact_person_mobile = request.data['contact_person_mobile']
    else:
        error_message['contactPersonMobile'] = ["This field is required"]

    if 'contact_person_email' in request.data:
        contact_person_email = request.data['contact_person_email']
    else:
        error_message['contactPersonEmail'] = ["This field is required"]
    if len(error_message) != 0:
        content['message'] = 'Invalid data'
        content['error'] = error_message
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
    try:
        company = Company.objects.get(pk=user_id)
    except:
        content['message'] = 'Company Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    # try:
    #     country = Country.objects.get(pk=country_id)
    # except:
    #     content['message'] = 'Country Not Found'
    #     return JsonResponse(content, status=status.HTTP_200_OK)
    try:
        industry = Industry.objects.get(pk=industry_id)
    except:
        content['message'] = 'Industry Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
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
    country, city, state = get_address_details(zip_code)
    company.company_name = company_name
    company.company_email = company_email
    company.phone_number = phone_number
    company.about_company = about_company
    company.company_size = company_size
    company.industry = industry
    company.country = country
    company.state = state
    company.city = city
    if 'company_website' in request.data:
        company_website = request.data['company_website']
        company.company_website = company_website
    # company.area = area
    company.contact_person_name = contact_person_name
    company.company_address_line_1 = address
    company.zip_code = zip_code
    company.contact_person_position = contact_person_position
    company.contact_person_mobile = contact_person_mobile
    company.contact_person_email = contact_person_email
    if 'company_website' in request.data:
        company_website = request.data['company_website']
        company.company_website = company_website
    if 'company_size' in request.data:
        company_size = request.data['company_size']
        company.company_size = company_size
    company.save()
    content['status'] = 1
    content['message'] = "Update successful"
    return JsonResponse(content, status=status.HTTP_200_OK)
    # if all(k in request.data for k in ("user_id", "industry_id", "address",
    #                                    "country_id", "state_id", "city_id", "area_id", "zip_code",
    #                                    "contact_person_name", "contact_person_position", "contact_person_mobile",
    #                                    "contact_person_email")):
    #     user_id = request.data['user_id']
    #     country_id = request.data['country_id']
    #     state_id = request.data['state_id']
    #     city_id = request.data['city_id']
    #     area_id = request.data['area_id']
    #     industry_id = request.data['industry_id']
    #     address = request.data['address']
    #     zip_code = request.data['zip_code']
    #     contact_person_name = request.data['contact_person_name']
    #     contact_person_mobile = request.data['contact_person_mobile']
    #     contact_person_email = request.data['contact_person_email']
    #     contact_person_position = request.data['contact_person_position']
    #     try:
    #         company = Company.objects.get(pk=user_id)
    #     except:
    #         content['message'] = 'Company Not Found'
    #         return JsonResponse(content, status=status.HTTP_200_OK)
    #     try:
    #         country = Country.objects.get(pk=country_id)
    #     except:
    #         content['message'] = 'Country Not Found'
    #         return JsonResponse(content, status=status.HTTP_200_OK)
    #     try:
    #         industry = Industry.objects.get(pk=industry_id)
    #     except:
    #         content['message'] = 'Industry Not Found'
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
    #     company.industry = industry
    #     company.country = country
    #     company.state = state
    #     company.city = city
    #     company.area = area
    #     company.contact_person_name = contact_person_name
    #     company.company_address_line_1 = address
    #     company.zip_code = zip_code
    #     company.contact_person_position = contact_person_position
    #     company.contact_person_mobile = contact_person_mobile
    #     company.contact_person_email = contact_person_email
    #     if 'company_website' in request.data:
    #         company_website = request.data['company_website']
    #         company.company_website = company_website
    #     if 'company_size' in request.data:
    #         company_size = request.data['company_size']
    #         company.company_size = company_size
    #     company.save()
    #     content['status'] = 1
    #     content['message'] = "Update successful"
    #     return JsonResponse(content, status=status.HTTP_200_OK)
    # else:
    #     content['message'] = "Provide Require Parameters"
    #     return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_all_job_by_company(request, company_id):
    content = {
        'status': 0
    }
    try:
        company = Company.objects.get(pk=company_id)
    except:
        content['message'] = 'Company Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    query_params = request.query_params
    company_jobs = Job.objects.filter(company=company, job_status=2)
    if "status" in query_params:
        req_status = query_params['status']
        if req_status == 'old':
            company_jobs = company_jobs.filter(application_deadline__lt=datetime.now())
        if req_status == 'recent':
            company_jobs = company_jobs.filter(application_deadline__gte=datetime.now())
    serialized_jobs = JobSerializer(company_jobs, many=True, context={'request': request})
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_applied_candidate(request, company_id, job_id):
    content = {
        'status': 0
    }
    try:
        company = Company.objects.get(pk=company_id)
    except:
        content['message'] = 'Company Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    try:
        job = Job.objects.get(pk=job_id)
    except:
        content['message'] = 'Job Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    # worker_ids = list(
    #     JobApplication.objects.filter(job_id=job, job_id__company=company).values_list('worker_id', flat=True))
    # workers = Worker.objects.filter(pk__in=worker_ids)
    # serialized_jobs = WorkerDetailsSerializer(workers, many=True, context={'request': request})
    applied_workers = JobApplication.objects.filter(job_id=job, job_id__company=company)
    worker_ids = list(applied_workers.values_list('worker_id', flat=True))
    workers = Worker.objects.filter(pk__in=worker_ids)
    send_data = []
    for applied_worker in applied_workers:
        worker = workers.get(pk=applied_worker.worker_id.id)
        serialized_worker = WorkerDetailsSerializer(worker, context={'request': request})
        short_list_status = {'is_shortlisted': applied_worker.is_short_listed}
        short_list_status.update(serialized_worker.data)
        send_data.append(short_list_status)
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = send_data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def company_make_candidate_shortlist(request):
    content = {
        'status': 0
    }
    if 'job_id' in request.data and 'worker_id' in request.data:
        job_id = request.data['job_id']
        worker_id = request.data['worker_id']
        try:
            job = Job.objects.get(pk=job_id)
        except:
            content['message'] = 'Job Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            worker = Worker.objects.get(pk=worker_id)
        except:
            content['message'] = 'Worker Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            worker_job = JobApplication.objects.get(job_id=job, worker_id=worker)
            worker_job.is_short_listed = True
            worker_job.save()
            content['status'] = 1
            content['message'] = 'Successful'
            return JsonResponse(content, status=status.HTTP_200_OK)
        except:
            content['message'] = 'Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_shortlisted_candidate(request, company_id, job_id):
    content = {
        'status': 0
    }
    try:
        company = Company.objects.get(pk=company_id)
    except:
        content['message'] = 'Company Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    try:
        job = Job.objects.get(pk=job_id)
    except:
        content['message'] = 'Job Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    worker_ids = list(
        JobApplication.objects.filter(job_id=job, job_id__company=company, is_short_listed=True).values_list(
            'worker_id', flat=True))
    workers = Worker.objects.filter(pk__in=worker_ids)
    serialized_jobs = WorkerSerializer(workers, many=True, context={'request': request})
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = serialized_jobs.data
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def company_get_job_statistic(request, company_id):
    content = {
        'status': 0
    }
    try:
        company = Company.objects.get(pk=company_id)
    except:
        content['message'] = 'Company Not Found'
        return JsonResponse(content, status=status.HTTP_200_OK)
    posted_jobs = Job.objects.filter(company=company)
    total_jobs = posted_jobs.count()
    running_jobs = posted_jobs.filter(application_deadline__gte=datetime.now()).count()
    expired_jobs = posted_jobs.filter(application_deadline__lt=datetime.now()).count()
    content['status'] = 1
    content['message'] = 'Success'
    content['data'] = {
        "total_jobs": total_jobs,
        "running_jobs": running_jobs,
        "expired_jobs": expired_jobs
    }
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def company_re_post_job(request):
    content = {
        'status': 0
    }
    if 'company_id' in request.data and 'job_id' in request.data and 'application_deadline' in request.data:
        company_id = request.data['company_id']
        job_id = request.data['job_id']
        application_deadline = request.data['application_deadline']
        try:
            company = Company.objects.get(pk=company_id)
        except:
            content['message'] = 'Company Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            company_job = Job.objects.get(pk=job_id)
            company_job.application_deadline = application_deadline
            company_job.save()
            content['status'] = 1
            content['message'] = 'Job Repost Successful'
            return JsonResponse(content, status=status.HTTP_200_OK)
        except:
            content['message'] = 'Something wrong'
            return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Require parameter missing'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def upload_company_logo(request):
    content = {
        'status': 0
    }
    if 'company_id' in request.data and 'logo' in request.data:
        company_id = request.data['company_id']
        try:
            company = Company.objects.get(pk=company_id)
        except:
            content['message'] = 'Company Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        logo = request.FILES.get('logo', False)
        if logo is not False:
            company.company_logo = logo
            company.save()
        else:
            content['message'] = 'Require File'
            return JsonResponse(content, status=status.HTTP_200_OK)
        content['status'] = 1
        content['message'] = 'Successful'
        return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def company_delete_job(request):
    content = {
        'status': 0
    }
    if 'company_id' in request.data and 'job_id' in request.data:
        company_id = request.data['company_id']
        job_id = request.data['job_id']
        try:
            company = Company.objects.get(pk=company_id)
        except:
            content['message'] = 'Company Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
        try:
            job = Job.objects.get(pk=job_id)
            job.job_status = 4
            job.save()
            content['status'] = 1
            content['message'] = 'Job Delete Successful'
            return JsonResponse(content, status=status.HTTP_200_OK)
        except:
            content['message'] = 'Job Not Found'
            return JsonResponse(content, status=status.HTTP_200_OK)
    else:
        content['message'] = 'Parameter Missing!'
        return JsonResponse(content, status=status.HTTP_200_OK)
