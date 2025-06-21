# Deployment Handoff Log

## Database Setup

- Configured Render managed PostgreSQL database for persistent user data storage.
- Purchased the $6.30/month PostgreSQL plan with 1 GB SSD storage.
- Added the `DATABASE_URL` environment variable to the Render web service for seamless database connection.
- Successfully ran Django migrations on Render to apply the database schema.

## Hosting Setup

- Using Render paid plan ($7/month) for web service hosting with instant start-up and 24/7 uptime.
- Total monthly cost for hosting and database: approximately $13.30.

## Notes

- Local development uses SQLite by default; production uses PostgreSQL on Render.
- Migrations must be run on Render environment to apply schema changes to the PostgreSQL database.
- Shell access on Render requires paid plan; migrations were run via Render shell after purchase.
- Database storage usage is currently ~6.46% of 1 GB, mostly system and metadata tables.
