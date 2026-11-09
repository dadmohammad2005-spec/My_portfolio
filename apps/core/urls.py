from django.urls import path
from .views import (
    HomeView,
    AboutView,
    CareersView,
    ScholarshipsView,
    ResumeView,
    DownloadResumeView,
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('careers/', CareersView.as_view(), name='careers'),
    path('scholarships/', ScholarshipsView.as_view(), name='scholarships'),
    path('resume/', ResumeView.as_view(), name='resume'),
    path('resume/download/', DownloadResumeView.as_view(), name='download_resume'),
]
