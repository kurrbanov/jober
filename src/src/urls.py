from django.contrib import admin
from django.urls import path
from jober import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('applicant/', views.ApplicantView.as_view()),
    path('company/', views.CompanyView.as_view()),
    path('like/company/', views.LikeToCompany.as_view()),
    path('like/applicant/', views.LikeToApplicant.as_view()),
    path('dislike/appicant/', views.DislikeToApplicant.as_view()),
    path('dislike/company/', views.DislikeToCompany.as_view()),
    path('show/applicant/', views.GetApplicant.as_view()),
    path('show/company/', views.GetCompanies.as_view()),
    path('applicant/<int:applicant_id>', views.ApplicantUpdateView.as_view()),
    path('company/<int:company_id>', views.CompanyUpdateView.as_view()),
    path('applicant/<int:applicant_id>', views.ApplicantDeleteView.as_view()),
    path('company/<int:company_id>', views.CompanyDeleteView.as_view())
]
