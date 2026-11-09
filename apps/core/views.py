from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.http import HttpResponse, Http404
from .models import SiteSettings, Skill, Experience, Education, Certification
from apps.projects.models import Project
from apps.blog.models import BlogPost

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_skills'] = Skill.objects.filter(is_featured=True)[:8]
        context['all_skills'] = Skill.objects.all()
        context['featured_projects'] = Project.objects.filter(is_featured=True).select_related('category')[:8]
        # Fallback to latest projects if none marked featured
        if not context['featured_projects']:
            context['featured_projects'] = Project.objects.select_related('category')[:8]
        context['all_projects'] = Project.objects.select_related('category')[:12]
        context['experiences'] = Experience.objects.all()[:3]
        context['latest_posts'] = BlogPost.objects.filter(is_published=True)[:3]
        return context


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_skills = Skill.objects.all()
        context['skills_by_category'] = {
            'programming': all_skills.filter(category='programming'),
            'backend': all_skills.filter(category='backend'),
            'database': all_skills.filter(category='database'),
            'tools': all_skills.filter(category='tools'),
            'ai': all_skills.filter(category='ai'),
            'frontend': all_skills.filter(category='frontend'),
        }
        context['all_skills'] = all_skills
        context['proficient_skills'] = all_skills.filter(tier='proficient')
        context['working_skills'] = all_skills.filter(tier='working')
        context['learning_skills'] = all_skills.filter(tier='learning')
        context['experiences'] = Experience.objects.all()
        context['educations'] = Education.objects.all()
        context['certifications'] = Certification.objects.all()
        return context


class CareersView(TemplateView):
    template_name = 'careers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.contact.forms import ContactForm
        context['contact_form'] = ContactForm()
        context['experiences'] = Experience.objects.all()
        context['educations'] = Education.objects.all()
        context['certifications'] = Certification.objects.all()
        context['projects'] = Project.objects.all()
        all_skills = Skill.objects.all()
        context['proficient_skills'] = all_skills.filter(tier='proficient')
        context['working_skills'] = all_skills.filter(tier='working')
        context['learning_skills'] = all_skills.filter(tier='learning')
        return context


class ScholarshipsView(TemplateView):
    template_name = 'scholarships.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.contact.forms import ContactForm
        context['contact_form'] = ContactForm()
        context['educations'] = Education.objects.all()
        context['certifications'] = Certification.objects.all()
        context['projects'] = Project.objects.all()
        return context


class ResumeView(TemplateView):
    template_name = 'resume.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = Experience.objects.all()
        context['educations'] = Education.objects.all()
        context['skills'] = Skill.objects.all()
        context['certifications'] = Certification.objects.all()
        context['projects'] = Project.objects.all()
        return context


class DownloadResumeView(View):
    def get(self, request, *args, **kwargs):
        settings_obj = SiteSettings.load()
        if settings_obj and settings_obj.resume_file:
            response = HttpResponse(settings_obj.resume_file, content_type='application/pdf')
            filename = f"{settings_obj.name.replace(' ', '_')}_Resume.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        # If no custom PDF uploaded, redirect to the HTML resume view with print dialog option
        return redirect('core:resume')
