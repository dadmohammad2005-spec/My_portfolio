import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Automatic database bootstrap for Render / Cloud deployments
# Ensures migrations are applied and initial portfolio data is loaded even if the build script was skipped
try:
    django.setup()
    from django.core.management import call_command
    call_command('migrate', interactive=False)
    
    from apps.projects.models import Project
    if not Project.objects.exists():
        call_command('loaddata', 'fixtures/initial_data.json')
except Exception as e:
    print(f"[WSGI Startup Bootstrap Notice]: {e}")

application = get_wsgi_application()
