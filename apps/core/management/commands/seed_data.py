import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.core.models import SiteSettings, Skill, Experience, Education
from apps.projects.models import Category, Project, ProjectScreenshot
from apps.blog.models import BlogPost

class Command(BaseCommand):
    help = "Seeds database with comprehensive, realistic sample data for the portfolio"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding portfolio data..."))

        # 1. Site Settings
        settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
        settings_obj.name = "Dad Mohammad"
        settings_obj.title = "Software Engineer"
        settings_obj.short_bio = (
            "I design and engineer robust, high-performance web applications, "
            "scalable backend systems, and modern user experiences with Python, Django, HTML5, CSS3, and JavaScript."
        )
        settings_obj.detailed_bio = (
            "I am a passionate Software Engineer specializing in Python, Django, and modern full-stack web architectures. "
            "I have deep expertise building resilient backend services, designing secure RESTful APIs, optimizing relational databases like PostgreSQL, "
            "and crafting responsive, accessible user interfaces with HTML5 and modern CSS3.\n\n"
            "I believe high-quality engineering comes from writing clean, testable code, adhering to SOLID principles, "
            "and continuously optimizing for security, performance, and user delight."
        )
        settings_obj.profile_photo = "profile/dad_mohammad_profile.jpg"
        settings_obj.resume_file = "resume/Dad_Mohammad_Resume.pdf"
        settings_obj.location = "Quetta, Balochistan, Pakistan"
        settings_obj.email = "dadmohammad2005@gmail.com"
        settings_obj.phone = "+92 310 8778900"
        settings_obj.github_url = "https://github.com/dadmohammad2005-spec"
        settings_obj.linkedin_url = "https://linkedin.com"
        settings_obj.twitter_url = "https://twitter.com"
        settings_obj.is_available_for_hire = True
        settings_obj.hero_badge_text = "Available for full-time engineering & consulting"
        settings_obj.years_of_experience = 5
        settings_obj.projects_completed = 20
        settings_obj.satisfied_clients = 15
        settings_obj.meta_keywords = "Dad Mohammad, Software Engineer, Python, Django, HTML5, CSS3, JavaScript, PostgreSQL, Portfolio"
        settings_obj.meta_description = (
            "Personal portfolio of Dad Mohammad - Software Engineer specializing in Python, Django, HTML5, CSS3, and scalable web architectures."
        )
        settings_obj.save()
        self.stdout.write(self.style.SUCCESS("[OK] Site settings configured."))
        # 2. Skills
        skills_data = [
            # Backend
            {"name": "Python 3 & Django / DRF", "category": "backend", "proficiency": 98, "icon": "server", "is_featured": True, "order": 1},
            {"name": "FastAPI & Asynchronous Python", "category": "backend", "proficiency": 90, "icon": "zap", "is_featured": True, "order": 2},
            {"name": "RESTful & GraphQL API Design", "category": "backend", "proficiency": 95, "icon": "network", "is_featured": True, "order": 3},
            {"name": "Celery & Distributed Task Queues", "category": "backend", "proficiency": 88, "icon": "layers", "is_featured": False, "order": 4},
            {"name": "Microservices & Distributed Systems", "category": "backend", "proficiency": 86, "icon": "cpu", "is_featured": False, "order": 5},
            
            # Frontend
            {"name": "JavaScript (ES6+) & TypeScript", "category": "frontend", "proficiency": 92, "icon": "code", "is_featured": True, "order": 6},
            {"name": "React & Next.js", "category": "frontend", "proficiency": 90, "icon": "layout", "is_featured": True, "order": 7},
            {"name": "Tailwind CSS & Modern CSS3", "category": "frontend", "proficiency": 94, "icon": "palette", "is_featured": False, "order": 8},
            {"name": "Semantic HTML5 & Web Accessibility (a11y)", "category": "frontend", "proficiency": 96, "icon": "eye", "is_featured": False, "order": 9},

            # Database
            {"name": "PostgreSQL & Query Optimization", "category": "database", "proficiency": 94, "icon": "database", "is_featured": True, "order": 10},
            {"name": "Redis In-Memory Caching", "category": "database", "proficiency": 90, "icon": "hard-drive", "is_featured": True, "order": 11},
            {"name": "Database Schema Design & Migrations", "category": "database", "proficiency": 95, "icon": "table", "is_featured": False, "order": 12},

            # DevOps
            {"name": "Docker & Containerization", "category": "devops", "proficiency": 90, "icon": "box", "is_featured": True, "order": 13},
            {"name": "AWS (ECS, S3, RDS, CloudFront)", "category": "devops", "proficiency": 85, "icon": "cloud", "is_featured": False, "order": 14},
            {"name": "CI/CD Pipelines (GitHub Actions)", "category": "devops", "proficiency": 92, "icon": "git-branch", "is_featured": False, "order": 15},
            {"name": "Linux, Nginx & WhiteNoise", "category": "devops", "proficiency": 88, "icon": "terminal", "is_featured": False, "order": 16},

            # Tools
            {"name": "Git & GitOps Workflows", "category": "tools", "proficiency": 96, "icon": "git-commit", "is_featured": False, "order": 17},
            {"name": "PyTest & Automated Testing", "category": "tools", "proficiency": 92, "icon": "check-circle", "is_featured": False, "order": 18},
            {"name": "System Architecture & Documentation", "category": "tools", "proficiency": 94, "icon": "file-text", "is_featured": False, "order": 19},
        ]
        Skill.objects.all().delete()
        for item in skills_data:
            Skill.objects.create(**item)
        self.stdout.write(self.style.SUCCESS(f"[OK] Created {len(skills_data)} skills."))

        # 3. Experience
        Experience.objects.all().delete()
        experiences_data = [
            {
                "company": "Apex Cloud Technologies",
                "role": "Lead Full-Stack Engineer",
                "location": "San Francisco, CA (Hybrid)",
                "employment_type": "Full-Time",
                "start_date": datetime.date(2022, 3, 1),
                "end_date": None,
                "is_current": True,
                "description": (
                    "- Spearheaded architecture and backend services for multi-tenant enterprise SaaS platform serving 500,000+ monthly active users.\n"
                    "- Redesigned database querying patterns and added Redis tiered caching, decreasing 99th percentile API latency by 45%.\n"
                    "- Led a cross-functional team of 6 engineers; established code quality guidelines, PR standards, and automated CI/CD checks."
                ),
                "technologies": "Python, Django, PostgreSQL, Redis, Celery, Docker, React, AWS",
                "order": 1,
            },
            {
                "company": "Nexa Interactive",
                "role": "Senior Software Engineer",
                "location": "Austin, TX (Remote)",
                "employment_type": "Full-Time",
                "start_date": datetime.date(2020, 1, 1),
                "end_date": datetime.date(2022, 2, 28),
                "is_current": False,
                "description": (
                    "- Developed high-throughput REST APIs handling 15M+ daily requests with 99.98% uptime.\n"
                    "- Created interactive data analytics dashboards in React with real-time metrics streaming via WebSockets.\n"
                    "- Migrated monolithic background jobs to scalable, fault-tolerant Celery workers and dead-letter queue handlers."
                ),
                "technologies": "Django REST Framework, PostgreSQL, Docker, React, TypeScript, Redis",
                "order": 2,
            },
            {
                "company": "CodePulse Labs",
                "role": "Full-Stack Developer",
                "location": "Boston, MA",
                "employment_type": "Full-Time",
                "start_date": datetime.date(2018, 6, 1),
                "end_date": datetime.date(2019, 12, 31),
                "is_current": False,
                "description": (
                    "- Built core business modules, transactional notification systems, and Stripe subscription payment integrations.\n"
                    "- Crafted accessible, responsive frontend components following WCAG 2.1 AA standards.\n"
                    "- Wrote extensive PyTest and Jest unit/integration test suites achieving over 90% test coverage."
                ),
                "technologies": "Python, Django, JavaScript, SQLite, Stripe API, Bootstrap, Git",
                "order": 3,
            },
        ]
        for exp in experiences_data:
            Experience.objects.create(**exp)
        self.stdout.write(self.style.SUCCESS("[OK] Created experience timeline records."))

        # 4. Education
        Education.objects.all().delete()
        educations_data = [
            {
                "institution": "The Islamia University of Bahawalpur",
                "degree": "Bachelor of Science in Software Engineering (6th Semester)",
                "field_of_study": "Software Engineering",
                "start_year": 2023,
                "end_year": 2027,
                "grade_or_honors": "CGPA: 3.02 / 4.00",
                "description": "Relevant Coursework: Data Structures & Algorithms, Object-Oriented Analysis & Design, Database Engineering, Operating Systems, Machine Learning Foundations, Software Architecture, RESTful Distributed Systems.",
                "order": 1,
            },
        ]
        for edu in educations_data:
            Education.objects.create(**edu)
        self.stdout.write(self.style.SUCCESS("[OK] Created education records."))

        # 5. Project Categories
        Category.objects.all().delete()
        cat_fullstack = Category.objects.create(name="Full-Stack Web Apps", slug="full-stack")
        cat_backend = Category.objects.create(name="Backend & Cloud APIs", slug="backend-apis")
        cat_devops = Category.objects.create(name="DevOps & Infrastructure", slug="devops-infra")
        cat_ai = Category.objects.create(name="AI & Intelligent Systems", slug="ai-systems")
        self.stdout.write(self.style.SUCCESS("[OK] Created project categories."))

        # 6. Projects
        Project.objects.all().delete()
        projects_data = [
            {
                "title": "CloudScale: Multi-Tenant Enterprise SaaS Platform",
                "slug": "cloudscale-multitenant-saas-platform",
                "category": cat_fullstack,
                "tagline": "Enterprise multi-tenant subscription platform with automated Stripe billing, analytics dashboards, and fine-grained RBAC.",
                "description": (
                    "CloudScale is an enterprise-ready SaaS foundation engineered to support thousands of tenant organizations with complete data isolation.\n\n"
                    "### Architecture Highlights:\n"
                    "- **Tenant Isolation**: Row-level and schema-based multi-tenancy in PostgreSQL with automatic connection routing.\n"
                    "- **Billing Engine**: Complete Stripe Billing integration supporting tiered metered usage, custom invoices, and self-serve upgrade flows.\n"
                    "- **Role-Based Access Control**: Granular permission hierarchies (Owner, Admin, Member, Read-Only) enforced at both ORM and API levels.\n"
                    "- **Real-Time Analytics**: Event-driven tracking pipeline aggregating usage metrics into interactive SVG charts.\n\n"
                    "### Technical Stack:\n"
                    "Built with Python 3.12, Django 5.1, Django REST Framework, React 18, Tailwind CSS, PostgreSQL, Redis, Celery, and Docker."
                ),
                "technologies": "Django, Django REST Framework, PostgreSQL, Redis, Celery, React, Docker, Tailwind CSS",
                "featured_image": "projects/cloudscale.svg",
                "github_url": "https://github.com",
                "live_demo_url": "https://example.com/demo/cloudscale",
                "is_featured": True,
                "order": 1,
            },
            {
                "title": "DevPulse: Distributed Synthetic API & Uptime Monitor",
                "slug": "devpulse-distributed-uptime-monitor",
                "category": cat_backend,
                "tagline": "Global synthetic monitoring engine checking HTTP/gRPC endpoints every 60 seconds with instant multi-channel alerting.",
                "description": (
                    "DevPulse is an open distributed observability system designed to monitor uptime, SSL/TLS certificate expirations, and response latencies across worldwide endpoints.\n\n"
                    "### Key Capabilities:\n"
                    "- **High-Concurrency Workers**: Asynchronous probe execution utilizing Python asyncio and distributed Celery workers.\n"
                    "- **Smart Incident Triaging**: Eliminates false positives by requiring confirmation probes from multiple geographic regions before firing alerts.\n"
                    "- **Instant Multi-Channel Alerts**: Webhook dispatchers for Slack, Discord, PagerDuty, SMS, and Email.\n"
                    "- **Public Status Pages**: Customizable branded status pages showing real-time component health and historical incident logs."
                ),
                "technologies": "Python, Django, FastAPI, TimescaleDB, Redis, Docker, Celery, Prometheus",
                "featured_image": "projects/devpulse.svg",
                "github_url": "https://github.com",
                "live_demo_url": "https://example.com/demo/devpulse",
                "is_featured": True,
                "order": 2,
            },
            {
                "title": "NexusFlow: Distributed Task Orchestration & Queue Inspector",
                "slug": "nexusflow-distributed-task-orchestrator",
                "category": cat_devops,
                "tagline": "Real-time visual orchestrator for Celery and Redis clusters featuring dead-letter inspection, live replays, and task metrics.",
                "description": (
                    "NexusFlow provides engineers with clear visibility into their background workers and task queues.\n\n"
                    "### Features:\n"
                    "- **Worker Fleet Telemetry**: Live heartbeat visualization, CPU/RAM utilization metrics, and worker node scaling.\n"
                    "- **Dead-Letter Queue Management**: Inspect stack traces of failed tasks and safely trigger replay executions with modified arguments.\n"
                    "- **Workflow Dependency Graphs**: Chain and chord visualizers allowing developers to see complex multi-step pipelines as interactive flow diagrams."
                ),
                "technologies": "Django, Python, Celery, Redis, WebSockets, Chart.js, WhiteNoise, Gunicorn",
                "featured_image": "projects/nexusflow.svg",
                "github_url": "https://github.com",
                "live_demo_url": "https://example.com/demo/nexusflow",
                "is_featured": True,
                "order": 3,
            },
            {
                "title": "SmartDoc: AI Vector Search & Document Ingestion Engine",
                "slug": "smartdoc-ai-vector-search-engine",
                "category": cat_ai,
                "tagline": "Production RAG document pipeline with sliding-window chunking, dense vector embeddings, and hybrid semantic retrieval.",
                "description": (
                    "SmartDoc enables organizations to index large corpuses of PDF, DOCX, and Markdown files and execute sub-second hybrid keyword/semantic search queries.\n\n"
                    "### Innovations:\n"
                    "- **Smart Chunking**: Preserves tables, headers, and code snippets during parsing instead of naive character splitting.\n"
                    "- **Hybrid Retrieval**: Combines BM25 lexical ranking with cosine vector similarity for peak precision.\n"
                    "- **Source Attribution**: Returns cited source snippets with direct page anchors for zero-hallucination verification."
                ),
                "technologies": "Python, Django REST Framework, OpenAI Embeddings, ChromaDB, Celery, PostgreSQL",
                "featured_image": "projects/smartdoc.svg",
                "github_url": "https://github.com",
                "live_demo_url": "https://example.com/demo/smartdoc",
                "is_featured": True,
                "order": 4,
            },
            {
                "title": "FinTrack: Modern Wealth & Portfolio Optimization Engine",
                "slug": "fintrack-wealth-portfolio-tracker",
                "category": cat_fullstack,
                "tagline": "Privacy-first personal wealth dashboard with bank aggregation, multi-asset allocation modeling, and retirement forecasting.",
                "description": (
                    "FinTrack is a privacy-conscious financial companion featuring bank integrations, currency conversions, asset allocation drift alerts, and Monte Carlo retirement simulations."
                ),
                "technologies": "Django, Django REST Framework, React, PostgreSQL, Tailwind CSS, Plaid API",
                "featured_image": "projects/fintrack.svg",
                "github_url": "https://github.com",
                "live_demo_url": "",
                "is_featured": False,
                "order": 5,
            },
            {
                "title": "GitDeploy: Zero-Downtime Container Deployment CLI",
                "slug": "gitdeploy-container-deployment-cli",
                "category": cat_devops,
                "tagline": "Lightweight developer CLI tool that manages automated staging-to-production Docker rollouts with instant rollbacks.",
                "description": (
                    "Command-line utility and webhook server automating Git push-to-deploy workflows on bare-metal and VPS instances without the complexity of Kubernetes."
                ),
                "technologies": "Python, Click, Docker Engine API, Bash, Nginx, Systemd",
                "featured_image": "projects/gitdeploy.svg",
                "github_url": "https://github.com",
                "live_demo_url": "",
                "is_featured": False,
                "order": 6,
            },
        ]
        for pdata in projects_data:
            Project.objects.create(**pdata)
        self.stdout.write(self.style.SUCCESS(f"[OK] Created {len(projects_data)} projects."))

        # 7. Blog Posts
        BlogPost.objects.all().delete()
        blogs_data = [
            {
                "title": "Architecting Scalable Django Applications for 1M+ Daily Requests",
                "slug": "architecting-scalable-django-applications-million-requests",
                "category": "Architecture",
                "tags": "Django, Python, Performance, PostgreSQL, Redis",
                "excerpt": "Key architectural strategies for optimizing Django ORM queries, configuring connection pooling, implementing multi-layer Redis caching, and decoupling heavy workloads.",
                "content": (
                    "Scaling a Django application to handle millions of requests every day requires moving beyond basic tutorials and understanding how the framework interacts with the database, operating system, and cache layers.\n\n"
                    "### 1. Master the ORM and Stop the N+1 Query Problem\n"
                    "The number one cause of sluggish Django applications is unoptimized ORM usage. Always use `select_related()` for single-valued relationships (ForeignKey, OneToOne) and `prefetch_related()` for multi-valued relationships (ManyToMany, reverse ForeignKeys).\n\n"
                    "```python\n"
                    "# Avoid:\n"
                    "projects = Project.objects.all()\n"
                    "for p in projects:\n"
                    "    print(p.category.name)  # Causes 1 query per project!\n\n"
                    "# Preferred:\n"
                    "projects = Project.objects.select_related('category').all()\n"
                    "```\n\n"
                    "### 2. Database Connection Pooling (`CONN_MAX_AGE`)\n"
                    "By default, Django closes the database connection at the end of each HTTP request. Establishing a new TCP and TLS handshake with PostgreSQL for every request adds significant overhead. Setting `CONN_MAX_AGE = 600` keeps connections alive across requests, slashing latency.\n\n"
                    "### 3. Asynchronous Task Offloading\n"
                    "Never perform I/O-heavy operations (sending emails, processing image uploads, calling external APIs) inside the request-response lifecycle. Offload them to background workers via Celery or Django channels.\n\n"
                    "### Summary\n"
                    "With query optimization, connection pooling, and asynchronous queuing, a single Django instance can easily sustain hundreds of requests per second with sub-50ms response times."
                ),
                "read_time": 7,
                "is_published": True,
                "published_date": timezone.now() - datetime.timedelta(days=3),
            },
            {
                "title": "The Senior Engineer's Guide to Zero-Downtime Database Migrations",
                "slug": "senior-engineers-guide-zero-downtime-database-migrations",
                "category": "Database",
                "tags": "PostgreSQL, Django, Migrations, DevOps, CI/CD",
                "excerpt": "How to modify database schemas on live production systems without table locks, downtime, or breaking active user sessions.",
                "content": (
                    "Running `python manage.py migrate` in production without understanding table locks can inadvertently lock your main tables and take your entire application down. Here is how to execute schema migrations safely.\n\n"
                    "### The Three-Phase Migration Pattern (Expand / Contract)\n"
                    "When renaming a column or changing a constraint, never do it in a single step.\n\n"
                    "1. **Phase 1 (Expand)**: Add the new column as nullable. Deploy the code that writes to both old and new columns, but reads from the old.\n"
                    "2. **Phase 2 (Backfill)**: Run a background migration to copy historical data from the old column to the new column in small batches.\n"
                    "3. **Phase 3 (Contract)**: Deploy code that reads and writes strictly from the new column. Once verified, drop the old column.\n\n"
                    "### Beware of Adding Defaults to Existing Columns\n"
                    "In older PostgreSQL versions, adding a column with a default value causes an entire table rewrite with an exclusive lock. Always add nullable columns first, backfill defaults, and then enforce constraints."
                ),
                "read_time": 6,
                "is_published": True,
                "published_date": timezone.now() - datetime.timedelta(days=12),
            },
            {
                "title": "Why Modern Python 3.12 Type Hints and Protocols Transform Codebases",
                "slug": "why-modern-python-type-hints-protocols-transform-codebases",
                "category": "Python",
                "tags": "Python 3.12, Clean Code, Architecture, Typing, Testing",
                "excerpt": "How static type checking with Mypy and structural subtyping with Protocols catch edge cases early and produce self-documenting code.",
                "content": (
                    "Python's dynamic typing is wonderful for rapid prototyping, but as codebases grow beyond tens of thousands of lines and dozens of contributors, type ambiguity becomes a major source of bugs.\n\n"
                    "### Structural Subtyping with `typing.Protocol`\n"
                    "Instead of rigid class inheritance, Python Protocols give you compile-time duck typing. If an object has the required methods, it satisfies the interface.\n\n"
                    "```python\n"
                    "from typing import Protocol\n\n"
                    "class Notifier(Protocol):\n"
                    "    def send(self, recipient: str, message: str) -> bool:\n"
                    "        ...\n"
                    "```\n\n"
                    "Now any class implementing `send` seamlessly fulfills `Notifier`, making unit testing and dependency injection effortless."
                ),
                "read_time": 5,
                "is_published": True,
                "published_date": timezone.now() - datetime.timedelta(days=25),
            },
        ]
        for bdata in blogs_data:
            BlogPost.objects.create(**bdata)
        self.stdout.write(self.style.SUCCESS(f"[OK] Created {len(blogs_data)} blog posts."))

        self.stdout.write(self.style.SUCCESS("\n[OK] Portfolio database seeded successfully!"))
