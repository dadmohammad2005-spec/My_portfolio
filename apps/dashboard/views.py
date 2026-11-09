from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.utils import timezone

from apps.projects.models import Project, Category
from apps.blog.models import BlogPost
from apps.core.models import Skill, Experience, Education, SiteSettings
from apps.contact.models import ContactMessage
from .forms import (
    DashboardLoginForm, ProjectForm, BlogPostForm,
    SkillForm, ExperienceForm, EducationForm, SiteSettingsForm
)


def staff_required(view_func):
    """Ensure user is logged in and is staff or superuser."""
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_staff or u.is_superuser),
        login_url='dashboard:login',
        redirect_field_name='next'
    )
    return actual_decorator(view_func)


# ==============================================================================
# Authentication Views
# ==============================================================================

def dashboard_login(request):
    """Dedicated login view for portfolio dashboard."""
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:home')

    next_url = request.GET.get('next', 'dashboard:home')
    if request.method == 'POST':
        form = DashboardLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or user.is_superuser:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect(request.POST.get('next') or 'dashboard:home')
            else:
                messages.error(request, "Access restricted to staff administrators.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = DashboardLoginForm(request)

    return render(request, 'dashboard/login.html', {
        'form': form,
        'next': next_url,
    })


def dashboard_logout(request):
    """Logout view for portfolio dashboard."""
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('dashboard:login')


# ==============================================================================
# Main Dashboard Overview
# ==============================================================================

@staff_required
def dashboard_home(request):
    """Comprehensive admin dashboard summary."""
    # Key Metrics
    total_projects = Project.objects.count()
    featured_projects = Project.objects.filter(is_featured=True).count()
    completed_projects = Project.objects.filter(status='completed').count()

    total_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(is_published=True).count()
    draft_posts = total_posts - published_posts

    total_skills = Skill.objects.count()
    total_experiences = Experience.objects.count()

    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()

    # Recent Records
    recent_messages = ContactMessage.objects.all()[:5]
    recent_projects = Project.objects.all()[:5]
    recent_posts = BlogPost.objects.all()[:4]

    context = {
        'stats': {
            'total_projects': total_projects,
            'featured_projects': featured_projects,
            'completed_projects': completed_projects,
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'total_skills': total_skills,
            'total_experiences': total_experiences,
            'total_messages': total_messages,
            'unread_messages': unread_messages,
        },
        'recent_messages': recent_messages,
        'recent_projects': recent_projects,
        'recent_posts': recent_posts,
        'active_menu': 'overview',
    }
    return render(request, 'dashboard/index.html', context)


# ==============================================================================
# Projects Management
# ==============================================================================

@staff_required
def projects_list(request):
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    category_id = request.GET.get('category', '').strip()

    projects = Project.objects.select_related('category').all()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(tagline__icontains=query) |
            Q(technologies__icontains=query)
        )
    if status_filter:
        projects = projects.filter(status=status_filter)
    if category_id:
        projects = projects.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        'projects': projects,
        'categories': categories,
        'query': query,
        'status_filter': status_filter,
        'category_id': category_id,
        'active_menu': 'projects',
    }
    return render(request, 'dashboard/projects/list.html', context)


@staff_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            messages.success(request, f"Project '{project.title}' created successfully!")
            return redirect('dashboard:projects_list')
    else:
        form = ProjectForm()

    return render(request, 'dashboard/projects/form.html', {
        'form': form,
        'title': 'Create New Project',
        'active_menu': 'projects',
    })


@staff_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, f"Project '{project.title}' updated successfully!")
            return redirect('dashboard:projects_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'dashboard/projects/form.html', {
        'form': form,
        'project': project,
        'title': f'Edit Project: {project.title}',
        'active_menu': 'projects',
    })


@staff_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f"Project '{title}' was deleted successfully.")
        return redirect('dashboard:projects_list')

    return render(request, 'dashboard/projects/confirm_delete.html', {
        'project': project,
        'active_menu': 'projects',
    })


@staff_required
@require_POST
def project_toggle_featured(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.is_featured = not project.is_featured
    project.save(update_fields=['is_featured'])
    status_str = "featured on homepage" if project.is_featured else "unpinned from homepage"
    messages.success(request, f"Project '{project.title}' is now {status_str}.")
    return redirect('dashboard:projects_list')


# ==============================================================================
# Blog Posts Management
# ==============================================================================

@staff_required
def blog_list(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    posts = BlogPost.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query) |
            Q(category__icontains=query)
        )
    if status == 'published':
        posts = posts.filter(is_published=True)
    elif status == 'draft':
        posts = posts.filter(is_published=False)

    context = {
        'posts': posts,
        'query': query,
        'status': status,
        'active_menu': 'blog',
    }
    return render(request, 'dashboard/blog/list.html', context)


@staff_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, f"Blog post '{post.title}' created successfully!")
            return redirect('dashboard:blog_list')
    else:
        form = BlogPostForm(initial={'published_date': timezone.now()})

    return render(request, 'dashboard/blog/form.html', {
        'form': form,
        'title': 'Write New Blog Post',
        'active_menu': 'blog',
    })


@staff_required
def blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, f"Post '{post.title}' updated successfully!")
            return redirect('dashboard:blog_list')
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'dashboard/blog/form.html', {
        'form': form,
        'post': post,
        'title': f'Edit Post: {post.title}',
        'active_menu': 'blog',
    })


@staff_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f"Post '{title}' was deleted successfully.")
        return redirect('dashboard:blog_list')

    return render(request, 'dashboard/blog/confirm_delete.html', {
        'post': post,
        'active_menu': 'blog',
    })


@staff_required
@require_POST
def blog_toggle_publish(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.is_published = not post.is_published
    post.save(update_fields=['is_published'])
    state = "published" if post.is_published else "moved to drafts"
    messages.success(request, f"Post '{post.title}' {state}.")
    return redirect('dashboard:blog_list')


# ==============================================================================
# Skills Management
# ==============================================================================

@staff_required
def skills_list(request):
    category = request.GET.get('category', '').strip()
    tier = request.GET.get('tier', '').strip()

    skills = Skill.objects.all()
    if category:
        skills = skills.filter(category=category)
    if tier:
        skills = skills.filter(tier=tier)

    context = {
        'skills': skills,
        'categories': Skill.CATEGORY_CHOICES,
        'tiers': Skill.TIER_CHOICES,
        'selected_category': category,
        'selected_tier': tier,
        'active_menu': 'skills',
    }
    return render(request, 'dashboard/skills/list.html', context)


@staff_required
def skill_create(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            messages.success(request, f"Skill '{skill.name}' added successfully!")
            return redirect('dashboard:skills_list')
    else:
        form = SkillForm()

    return render(request, 'dashboard/skills/form.html', {
        'form': form,
        'title': 'Add New Skill',
        'active_menu': 'skills',
    })


@staff_required
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill = form.save()
            messages.success(request, f"Skill '{skill.name}' updated successfully!")
            return redirect('dashboard:skills_list')
    else:
        form = SkillForm(instance=skill)

    return render(request, 'dashboard/skills/form.html', {
        'form': form,
        'skill': skill,
        'title': f'Edit Skill: {skill.name}',
        'active_menu': 'skills',
    })


@staff_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        name = skill.name
        skill.delete()
        messages.success(request, f"Skill '{name}' was deleted.")
        return redirect('dashboard:skills_list')

    return render(request, 'dashboard/skills/confirm_delete.html', {
        'skill': skill,
        'active_menu': 'skills',
    })


# ==============================================================================
# Experience & Education Management
# ==============================================================================

@staff_required
def experience_list(request):
    experiences = Experience.objects.all()
    educations = Education.objects.all()

    context = {
        'experiences': experiences,
        'educations': educations,
        'active_menu': 'experience',
    }
    return render(request, 'dashboard/experiences/list.html', context)


@staff_required
def experience_create(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save()
            messages.success(request, f"Experience at '{exp.company}' added!")
            return redirect('dashboard:experience_list')
    else:
        form = ExperienceForm()

    return render(request, 'dashboard/experiences/form.html', {
        'form': form,
        'title': 'Add Career Experience',
        'active_menu': 'experience',
    })


@staff_required
def experience_edit(request, pk):
    exp = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            exp = form.save()
            messages.success(request, f"Experience at '{exp.company}' updated!")
            return redirect('dashboard:experience_list')
    else:
        form = ExperienceForm(instance=exp)

    return render(request, 'dashboard/experiences/form.html', {
        'form': form,
        'experience': exp,
        'title': f'Edit Experience: {exp.company}',
        'active_menu': 'experience',
    })


@staff_required
def experience_delete(request, pk):
    exp = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        company = exp.company
        exp.delete()
        messages.success(request, f"Experience at '{company}' deleted.")
        return redirect('dashboard:experience_list')

    return render(request, 'dashboard/experiences/confirm_delete.html', {
        'item': exp,
        'type': 'Experience',
        'active_menu': 'experience',
    })


@staff_required
def education_create(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save()
            messages.success(request, f"Education record at '{edu.institution}' added!")
            return redirect('dashboard:experience_list')
    else:
        form = EducationForm()

    return render(request, 'dashboard/experiences/form.html', {
        'form': form,
        'title': 'Add Education Record',
        'active_menu': 'experience',
    })


@staff_required
def education_edit(request, pk):
    edu = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=edu)
        if form.is_valid():
            edu = form.save()
            messages.success(request, f"Education at '{edu.institution}' updated!")
            return redirect('dashboard:experience_list')
    else:
        form = EducationForm(instance=edu)

    return render(request, 'dashboard/experiences/form.html', {
        'form': form,
        'education': edu,
        'title': f'Edit Education: {edu.institution}',
        'active_menu': 'experience',
    })


@staff_required
def education_delete(request, pk):
    edu = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        inst = edu.institution
        edu.delete()
        messages.success(request, f"Education record for '{inst}' deleted.")
        return redirect('dashboard:experience_list')

    return render(request, 'dashboard/experiences/confirm_delete.html', {
        'item': edu,
        'type': 'Education',
        'active_menu': 'experience',
    })


# ==============================================================================
# Contact Messages Inbox
# ==============================================================================

@staff_required
def messages_list(request):
    status = request.GET.get('status', '').strip()
    query = request.GET.get('q', '').strip()

    messages_qs = ContactMessage.objects.all()

    if status == 'unread':
        messages_qs = messages_qs.filter(is_read=False)
    elif status == 'read':
        messages_qs = messages_qs.filter(is_read=True)

    if query:
        messages_qs = messages_qs.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(subject__icontains=query) |
            Q(message__icontains=query)
        )

    unread_count = ContactMessage.objects.filter(is_read=False).count()

    context = {
        'inbox_messages': messages_qs,
        'unread_count': unread_count,
        'status_filter': status,
        'query': query,
        'active_menu': 'messages',
    }
    return render(request, 'dashboard/messages/list.html', context)


@staff_required
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    # Automatically mark as read when viewed
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=['is_read'])

    return render(request, 'dashboard/messages/detail.html', {
        'message_obj': msg,
        'active_menu': 'messages',
    })


@staff_required
@require_POST
def message_toggle_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save(update_fields=['is_read'])
    state = "marked as read" if msg.is_read else "marked as unread"
    messages.success(request, f"Message from {msg.name} {state}.")
    return redirect('dashboard:messages_list')


@staff_required
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        name = msg.name
        msg.delete()
        messages.success(request, f"Message from {name} was deleted.")
        return redirect('dashboard:messages_list')

    return render(request, 'dashboard/messages/confirm_delete.html', {
        'message_obj': msg,
        'active_menu': 'messages',
    })


# ==============================================================================
# Site Settings Management
# ==============================================================================

@staff_required
def site_settings_edit(request):
    settings_obj = SiteSettings.load()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Portfolio identity & settings updated successfully!")
            return redirect('dashboard:site_settings_edit')
    else:
        form = SiteSettingsForm(instance=settings_obj)

    return render(request, 'dashboard/settings/form.html', {
        'form': form,
        'settings_obj': settings_obj,
        'active_menu': 'settings',
    })
