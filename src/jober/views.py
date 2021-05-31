from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import *

SKILLS = [
        ('1', 'Python'),
        ('2', 'Django'),
        ('3', 'DRF'),
        ('4', 'JavaScript'),
        ('5', 'VUE.js'),
        ('6', 'React'),
        ('7', 'C#'),
        ('8', 'ASP.NET'),
        ('9', 'Cooking')
]


class ApplicantView(APIView):
    serializer_class = ApplicantSerializer

    @staticmethod
    def get(request, *args, **kwargs):
        applicants = Applicant.objects.all()
        serializer = ApplicantShowSerializer(applicants, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, *args, **kwargs):
        changed_lst = request.data['skills']

        def find_num(val):
            for elem in SKILLS:
                if elem[1] == val:
                    return elem[0]

            return '-1'

        request.data['skills'] = [{"value": find_num(val)} for val in changed_lst]

        new_applicant = ApplicantSerializer(data=request.data)
        if new_applicant.is_valid():
            new_applicant.save()
        else:
            return Response(new_applicant.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(new_applicant.data, status=status.HTTP_201_CREATED)


class CompanyView(APIView):
    serializer_class = CompanySerializer

    @staticmethod
    def get(request, *args, **kwargs):
        companies = Company.objects.all()
        ser = CompanyShowSerializer(companies, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, *args, **kwargs):
        changed_lst = request.data['skills']

        def find_num(val):
            for elem in SKILLS:
                if elem[1] == val:
                    return elem[0]

            return '-1'

        request.data['skills'] = [{"value": find_num(val)} for val in changed_lst]

        new_company = CompanySerializer(data=request.data)
        if new_company.is_valid():
            new_company.save()
        else:
            return Response(new_company.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(new_company.data, status=status.HTTP_201_CREATED)


class LikeToCompany(APIView):
    """
    {
        "applicant_id": 1,
        "company_id": 3
    }
    """
    @staticmethod
    def post(request, *args, **kwargs):
        applicant = Applicant.objects.filter(id=request.data['applicant_id'])
        cmp = Company.objects.filter(id=request.data['company_id'])

        if len(applicant) == 0 or len(cmp) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        applicant = applicant[0]
        cmp = cmp[0]

        like = Like.objects.create(value=request.data['company_id'])
        like.save()
        applicant.likes.add(like)
        applicant.save()

        exist_match = cmp.likes.filter(value=request.data['applicant_id'])
        if len(exist_match) > 0:
            match_company = Match.objects.create(value=request.data['applicant_id'])
            match_company.save()
            cmp.matches.add(match_company)
            cmp.save()
            match_applicant = Match.objects.create(value=request.data['company_id'])
            match_applicant.save()
            applicant.matches.add(match_applicant)
            applicant.save()

        return Response({"Like to": request.data['company_id']}, status=status.HTTP_202_ACCEPTED)


class LikeToApplicant(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        company = Company.objects.filter(id=request.data['company_id'])
        apl = Applicant.objects.filter(id=request.data['applicant_id'])

        if len(company) == 0 or len(apl) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        company = company[0]
        apl = apl[0]

        like = Like.objects.create(value=request.data['applicant_id'])
        like.save()
        company.likes.add(like)
        company.save()

        exist_match = apl.likes.filter(value=request.data['company_id'])

        if len(exist_match) > 0:
            match_applicant = Match.objects.create(value=request.data['company_id'])
            match_applicant.save()
            apl.matches.add(match_applicant)
            apl.save()

            match_company = Match.objects.create(value=request.data['applicant_id'])
            match_company.save()
            company.matches.add(match_company)
            company.save()

        return Response({"Like to:": request.data['applicant_id']}, status=status.HTTP_202_ACCEPTED)


class GetCompanies(APIView):
    """
    Request:
    {
        "applicant_id": 1
    }

    Response:
    {
        id: [1, 2, ...]
    }

    Priority: Match, skills(at least one) + region, likes
    """
    @staticmethod
    def post(request, *args, **kwargs):
        applicant = Applicant.objects.filter(id=request.data['applicant_id'])

        if len(applicant) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        applicant = applicant[0]

        response_list = set()

        for match in applicant.matches.all():
            response_list.add(match.value)

        set_skills_apl = set()
        for skill in applicant.skills.all():
            set_skills_apl.add(skill.value)

        for company in Company.objects.all():
            set_skills_cmp = set()
            for skill in company.skills.all():
                set_skills_cmp.add(skill.value)

            if len(set_skills_apl & set_skills_cmp):
                if applicant.relocate:
                    response_list.add(company.id)
                else:
                    if company.region == applicant.region:
                        response_list.add(company.id)
            if company.likes.filter(value=applicant.id):
                response_list.add(company.id)

        return Response({"companies_id": list(response_list)}, status=status.HTTP_200_OK)


class GetApplicant(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        company = Company.objects.filter(id=request.data['company_id'])

        if len(company) < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        company = company[0]
        response_list = set()

        for match in company.matches.all():
            response_list.add(match.value)

        set_company_skills = set()

        for skill in company.skills.all():
            set_company_skills.add(skill.value)

        for applicant in Applicant.objects.all():
            set_applicant_skills = set()
            for skill in applicant.skills.all():
                set_applicant_skills.add(skill.value)

            if len(set_applicant_skills & set_company_skills):
                if applicant.region == company.region:
                    response_list.add(applicant.id)
                elif applicant.relocate:
                    response_list.add(applicant.id)
                else:
                    continue

            if applicant.likes.filter(value=company.id):
                response_list.add(applicant.id)

        return Response({"applicants_id": list(response_list)}, status=status.HTTP_200_OK)


class ValidSkills:
    @staticmethod
    def check(skill):
        for elem in SKILLS:
            if skill == elem[1]:
                return [True, elem[0]]

        return [False, -1]


class ApplicantUpdateView(APIView):
    @staticmethod
    def patch(request, applicant_id):
        applicant = Applicant.objects.filter(id=applicant_id)

        if len(applicant) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        applicant = applicant[0]

        for fields in request.data:
            if fields == 'name' or fields == 'surname':
                if len(request.data[fields]) > 25:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                if fields == 'name':
                    applicant.name = request.data[fields]
                else:
                    applicant.surname = request.data[fields]
            elif fields == 'skills':
                applicant.skills.clear()
                for skill in request.data[fields]:
                    if not ValidSkills.check(skill)[0]:
                        return Response(status=status.HTTP_400_BAD_REQUEST)

                for skill in request.data[fields]:
                    sk = Skill.objects.create(value=ValidSkills.check(skill)[1])
                    sk.save()
                    applicant.skills.add(sk)
                    applicant.save()
            elif fields == 'relocate':
                applicant.relocate = request.data[fields]
            elif fields == 'email':
                applicant.email = request.data[fields]
            elif fields == 'age':
                applicant.age = request.data[fields]
            elif fields == 'region':
                applicant.region = request.data[fields]

            applicant.save()

        return Response(ApplicantShowSerializer(Applicant.objects.filter(id=applicant_id)[0]).data,
                        status=status.HTTP_200_OK)


class CompanyUpdateView(APIView):
    @staticmethod
    def patch(request, company_id):
        company = Company.objects.filter(id=company_id)

        if len(company) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        company = company[0]

        for field in request.data:
            if field == 'name':
                if len(request.data['name']) > 25:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                company.name = request.data['name']
            elif field == 'skills':
                company.skills.clear()
                for skill in request.data[field]:
                    if not ValidSkills.check(skill)[0]:
                        return Response(status=status.HTTP_400_BAD_REQUEST)

                for skill in request.data[field]:
                    sk = Skill.objects.create(value=ValidSkills.check(skill)[1])
                    sk.save()
                    company.skills.add(sk)
                    company.save()
            elif field == 'age':
                company.age = request.data[field]
            elif field == 'region':
                company.region = request.data[field]
            elif field == 'desc':
                company.desc = request.data[field]

            company.save()

        return Response(CompanyShowSerializer(company).data, status=status.HTTP_200_OK)


class ApplicantDeleteView(APIView):
    @staticmethod
    def delete(request, applicant_id, *args, **kwargs):
        snippet = Applicant.objects.filter(id=applicant_id)
        if len(snippet) == 0:
            return Response({"Bad Request": "No applicant with such id"}, status=status.HTTP_400_BAD_REQUEST)

        snippet[0].delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyDeleteView(APIView):
    @staticmethod
    def delete(request, company_id, *args, **kwargs):
        snippet = Company.objects.filter(id=company_id)
        if len(snippet) == 0:
            return Response({"Bad Request": "No company with such id"}, status=status.HTTP_400_BAD_REQUEST)

        snippet[0].delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
