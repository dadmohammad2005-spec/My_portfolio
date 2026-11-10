from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Category, Project

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        qs = Project.objects.select_related('category').prefetch_related('screenshots').all()
        category_slug = self.request.GET.get('category')
        search_query = self.request.GET.get('q')

        if category_slug and category_slug != 'all':
            qs = qs.filter(category__slug=category_slug)

        if search_query:
            qs = qs.filter(
                Q(title__icontains=search_query) |
                Q(tagline__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(technologies__icontains=search_query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(projects__isnull=False).distinct()
        context['current_category'] = self.request.GET.get('category', 'all')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context['screenshots'] = project.screenshots.all()
        # Related projects from same category
        if project.category:
            context['related_projects'] = Project.objects.filter(
                category=project.category
            ).exclude(id=project.id)[:3]
        else:
            context['related_projects'] = Project.objects.exclude(id=project.id)[:3]
        return context
