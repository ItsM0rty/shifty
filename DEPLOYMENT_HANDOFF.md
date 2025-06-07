# Deployment and Development Handoff for Shifty Project

## Project Overview
- Backend: Django 5.2 with a custom User model and models for Shift scheduling, Availability, and TimeOffRequests.
- Frontend: Django templates with static assets (JS, CSS, images) served via WhiteNoise.
- Database: Supports SQLite for local dev and PostgreSQL for production.
- Deployment: Dockerized app intended for deployment on Render.com or Fly.io.

## Current Deployment Status
- The project is set up for deployment on Render.com using Docker.
- The Dockerfile installs dependencies and runs the app with Gunicorn.
- The Render Start Command should be cleared to allow the Dockerfile CMD to run properly.
- Database migrations and static file collection need to be run manually via the Render shell after deployment.

## How to Deploy on Render.com
1. Connect the GitHub repository to Render and create a new Web Service.
2. Leave the Start Command field empty in the Render service settings.
3. Add environment variables:
   - `DATABASE_URL`: Provided by Render’s managed Postgres service.
   - `SECRET_KEY`: Use the existing Django secret key or generate a new one.
4. Trigger a manual deploy.
5. After deployment completes, open the Render shell and run:
   ```
   python3 manage.py migrate --noinput
   python3 manage.py collectstatic --noinput
   ```
6. The site should then be live and accessible.

## Local Development Setup
1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run migrations locally with `python manage.py migrate`.
4. Start the development server with `python manage.py runserver`.
5. Use SQLite locally; no need for PostgreSQL unless testing production DB features.

## Notes for Next Developer
- The `Dockerfile` uses Python 3.10 and installs system dependencies including PostgreSQL client and SQLite.
- Static files are served using WhiteNoise.
- The `config/settings.py` file handles switching between SQLite (local) and PostgreSQL (production) based on environment variables.
- The custom user model is `myapp.User`.
- The project uses Gunicorn as the WSGI server in production.
- Migrations and static file collection are not automated in the current Render setup; they must be run manually or scripted.

## Recommendations
- Consider automating migrations and static file collection in the deployment process for smoother deploys.
- Monitor Render logs for errors and performance.
- Use Render’s dashboard for environment variable management and manual shell access.

---

This document should help you get started quickly with development and deployment of the Shifty project.
