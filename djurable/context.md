# `djurable` Project Structure
`djurable` is an opinionated Django ETL + streaming scaffold for building data ingestion pipelines, stream processors, and real-time orchestration services. It integrates Quix Streams, Django REST Framework, JWT authentication, and Django Channels out of the box.

Root Layout
```bash
project_root/
│
├── config/                   # Core Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Centralized settings
│   ├── urls.py               # Root URL routes
│   ├── wsgi.py
│   ├── setup.py              # Custom admin + widget auto-registration
│   ├── widgets.py            # Widget discovery & template tag registration
│   └── celery.py             # Celery app initialization
│
├── _api_config/              # DRF + JWT API-specific settings
│   ├── __init__.py
│   └── settings.py
│
├── _ws_config/               # Django Channels + WebSocket-specific settings
│   ├── __init__.py
│   └── routing.py
│
├── apps/                     # All Django apps for this service
│   ├── crawlers/             # Data ingestion from APIs, scrapers, etc.
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── ...
│   │
│   ├── streams/              # Quix Streams-powered stream processing
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── ...
│   │
│   └── <other_app>/          # Any other business/domain apps
│
├── requirements.txt          # Python dependencies
├── manage.py
└── context.md                # This explanation file
```

## Core Conventions

### config folder

Always named config (never project name).

Contains:

Django core setup.

Celery initialization (celery.py).

Custom admin setup (setup.py).

Widget auto-registration (widgets.py).

Special config folders

_api_config: Holds DRF + JWT-specific settings and overrides.

_ws_config: Holds WebSocket and Channels routing setup.

### apps folder

All business logic is in apps/.

Each app is a full Django app (with apps.py, models.py, admin.py, migrations, etc.).

Special apps:

crawlers: All ingestion scripts (API clients, scrapers, data collectors).

streams: All Quix Streams pipelines, event processing, and sinks.

Admin customization

setup.py in config auto-registers custom widget template tags from any app's widgets.py file.

Widgets must:

Inherit from django.forms.widgets.Widget.

Implement a static get_template_tag() method with metadata.

Stream Processing

Uses Quix Streams for real-time event ingestion and transformation.

Designed so each stream processor lives inside a Django app in streams/.

ETL Philosophy

Treat each pipeline stage as a Django app.

Scheduling handled by Celery Beat in the Django admin (no Airflow dependency).

Supports splitting large event processing workloads into separate microservices if needed.

Key Integrations
Django REST Framework — API layer.

djangorestframework-simplejwt — JWT authentication.

Quix Streams — Event streaming & pipelines.

Django Channels — Real-time WebSocket support.

Celery — Task queue & scheduled jobs.

unfold-admin — Modern admin interface.

