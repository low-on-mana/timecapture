# TimeCapture

A time tracking application using Docker, Django, and MariaDB.

## Quick Start

### 1. Copy settings
```bash
cp timecapture/settings.fake.py timecapture/settings.py
```

### 2. Start all services
```bash
docker compose up --build
```

### 3. Create a superuser
First, identify your web container:
```bash
docker ps
```

Then create the superuser (using the appropriate container name):
```bash
docker exec -it timecapture-web-1 python manage.py createsuperuser
```

### 4. Access the application
- **Admin interface**: http://localhost:8000/admin/
- **User portal**: http://localhost:8000/

## User Management
- Additional users can be created through the admin interface
- New users will receive the default password set in `DEFAULT_USER_PASSWORD` in `settings.py`

## Technical Notes
- **Database**: Uses MariaDB 10.5 instead of MySQL for better ARM processor compatibility
- **Ports**:
  - Application: 8000
  - Database: 3306

## Troubleshooting
If you encounter issues:
1. Verify all containers are running with `docker ps -a`
2. Check logs for specific containers:
```bash
docker logs timecapture-web-1
docker logs timecapture-db-1
```

## Requirements
- Docker
- Docker Compose
