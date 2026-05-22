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



# def contact(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name', '').strip()
#         last_name  = request.POST.get('last_name', '').strip()
#         email      = request.POST.get('email', '').strip()
#         subject    = request.POST.get('subject', '').strip()
#         message    = request.POST.get('message', '').strip()

#         if not all([first_name, last_name, email, subject, message]):
#             messages.error(request, 'Please fill in all required fields.')
#         else:
#             # ✅ Save to DB or send email here
#             messages.success(request, f'Thanks {first_name}! Your message has been sent successfully.')
#             return redirect('contact')

#     return render(request, 'main/contact.html')