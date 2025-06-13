from django.core.management.base import BaseCommand
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Tests database connection and basic queries'

    def handle(self, *args, **options):
        try:
            # Test raw connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                logger.info(f"Database connection test: SELECT 1 returned {result}")
            
            # Test ORM access
            from myapp.models import User
            count = User.objects.count()
            logger.info(f"Found {count} users in database")
            
            self.stdout.write(self.style.SUCCESS('Database connection test successful'))
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            self.stdout.write(self.style.ERROR(f'Database connection failed: {str(e)}'))