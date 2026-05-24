from django.shortcuts import render, redirect
from django.contrib import messages
from .models import About, Skill, Project, ContactMessage
from .forms import ContactForm

def home(request):
    context = {
        'about': About.objects.first(),
        'frontend_skills': Skill.objects.filter(category='frontend'),
        'backend_skills': Skill.objects.filter(category='backend'),
        'database_skills': Skill.objects.filter(category='database'),
        'tools_skills': Skill.objects.filter(category='tools'),
        'skills': Skill.objects.all(),
        'projects': Project.objects.all()[:6],  # Show latest 6 projects
    }
    return render(request, 'main/home.html', context)

def about(request):
    context = {
        'about': About.objects.first(),
    }
    return render(request, 'main/about.html', context)

def skills(request):
    context = {
        'frontend_skills': Skill.objects.filter(category='frontend'),
        'backend_skills': Skill.objects.filter(category='backend'),
        'database_skills': Skill.objects.filter(category='database'),
        'tools_skills': Skill.objects.filter(category='tools'),
        'skills': Skill.objects.all(),
    }
    return render(request, 'main/skills.html', context)

def projects(request):
    context = {
        'projects': Project.objects.all(),
    }
    return render(request, 'main/projects.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, 'Thank you! Your message has been sent successfully.')
        return redirect('main:contact')  # Using namespace
    
    context = {
        'about': About.objects.first(),
    }
    return render(request, 'main/contact.html', context)
